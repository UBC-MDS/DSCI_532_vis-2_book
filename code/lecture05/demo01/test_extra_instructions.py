"""Test: does the LLM call querychat_query or hallucinate stats?

Runs the same setup as app-07e, sends a filter request,
then inspects all turns to see what tool calls were made.
"""

from pathlib import Path

import querychat
from chatlas import ChatGithub, ContentToolRequest, ContentToolResult
from dotenv import load_dotenv
from seaborn import load_dataset

load_dotenv(Path(__file__).parent / ".env")

titanic = load_dataset("titanic")

EXTRA_INSTRUCTIONS = """
When filtering the data, always reply using EXACTLY this format — no exceptions:

🎯 **Filter:** [one sentence describing what was selected]
📊 **Stats:** use querychat_query to calculate row count and survival rate, then write: [N rows] | survival rate: [X%] | overall: 38.4%
💡 **Insight:** [one sentence interpreting whether this group survived better or worse than average]
🔍 **Try next:** <span class="suggestion">[a natural follow-up question]</span>
"""

qc = querychat.QueryChat(
    titanic,
    "titanic",
    extra_instructions=EXTRA_INSTRUCTIONS,
    client=ChatGithub(model="gpt-4.1-mini"),
)

# Get the chat client
def on_update(data):
    print(f"\n>>> CALLBACK: update_dashboard fired")
    print(f"    query: {data['query']}")
    print(f"    title: {data['title']}")

def on_reset():
    print(f"\n>>> CALLBACK: reset_dashboard fired")

chat = qc.client(update_dashboard=on_update, reset_dashboard=on_reset)

# Send the message
print("=" * 60)
print("USER: Show only first class passengers")
print("=" * 60)
response = chat.chat("Show only first class passengers", echo="none")
print(f"\nFINAL RESPONSE:\n{response}")

# Inspect ALL turns
print("\n" + "=" * 60)
print("FULL TURN HISTORY")
print("=" * 60)

turns = chat.get_turns()
print(f"\nTotal turns: {len(turns)}\n")

for i, turn in enumerate(turns):
    print(f"--- Turn {i} [{turn.role}] ---")
    for content in turn.contents:
        if isinstance(content, ContentToolRequest):
            # Use model_dump to safely get all fields
            d = content.model_dump()
            tool_name = d.get("name", d.get("function", "unknown"))
            args = d.get("arguments", d.get("input", {}))
            print(f"  🔧 TOOL CALL: {tool_name}")
            print(f"     args: {args}")
        elif isinstance(content, ContentToolResult):
            val = str(content.value)[:300] if content.value else "(empty)"
            print(f"  📥 TOOL RESULT: {val}")
        else:
            text = str(content)[:300]
            print(f"  💬 {text}")
    print()
