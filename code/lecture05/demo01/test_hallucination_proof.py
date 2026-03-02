"""Definitive test: does the LLM hallucinate stats or call querychat_query?

Uses a FAKE dataset the LLM cannot know from training.
If it still produces specific row counts and rates, it's hallucinating.

Run: .venv/bin/python test_hallucination_proof.py
"""

from pathlib import Path

import pandas as pd
import querychat
from chatlas import ChatGithub, ContentToolRequest, ContentToolResult
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# ── Fake dataset the LLM has NEVER seen ─────────────────────────────
fake_data = pd.DataFrame({
    "planet": ["Zorgon"] * 30 + ["Xylpha"] * 20 + ["Brimtak"] * 50,
    "survived_crash": [1]*18 + [0]*12 + [1]*5 + [0]*15 + [1]*35 + [0]*15,
    "crew_role": (["pilot"]*10 + ["medic"]*20 + ["pilot"]*8 + ["medic"]*12
                  + ["pilot"]*25 + ["medic"]*25),
    "age": list(range(20, 50)) + list(range(25, 45)) + list(range(18, 68)),
})
# Ground truth: Zorgon survival = 18/30 = 60%, overall = 58/100 = 58%

EXTRA_INSTRUCTIONS_NO_QUERY = """
Always reply using EXACTLY this format — no exceptions:

🎯 **Filter:** [one sentence describing what was selected]
📊 **Stats:** [N rows] | survival rate: [X%] | overall: 58%
💡 **Insight:** [one sentence]
"""

EXTRA_INSTRUCTIONS_WITH_QUERY = """
When filtering, always reply using EXACTLY this format — no exceptions:

🎯 **Filter:** [one sentence describing what was selected]
📊 **Stats:** FIRST call querychat_query to calculate count and survival rate, then write: [N rows] | survival rate: [X%] | overall: 58%
💡 **Insight:** [one sentence]
"""

def run_test(label, instructions):
    print(f"\n{'='*60}")
    print(f"TEST: {label}")
    print(f"{'='*60}")

    qc = querychat.QueryChat(
        fake_data, "crashes",
        extra_instructions=instructions,
        client=ChatGithub(model="gpt-4.1-mini"),
    )

    tool_calls_seen = []

    def on_update(data):
        tool_calls_seen.append(("update_dashboard", data["query"], data["title"]))
        print(f"  >>> update_dashboard: {data['query']}")

    def on_reset():
        tool_calls_seen.append(("reset_dashboard",))

    chat = qc.client(update_dashboard=on_update, reset_dashboard=on_reset)
    response = chat.chat("Show only Zorgon passengers", echo="none")

    print(f"\nRESPONSE:\n{response}")

    # Inspect turn history for ALL tool calls
    print(f"\nTOOL CALLS IN TURN HISTORY:")
    for i, turn in enumerate(chat.get_turns()):
        for content in turn.contents:
            if isinstance(content, ContentToolRequest):
                d = content.model_dump()
                name = d.get("name", "?")
                args = d.get("arguments", d.get("input", {}))
                tool_calls_seen.append(("turn_tool_request", name, args))
                print(f"  Turn {i}: {name}({args})")
            elif isinstance(content, ContentToolResult):
                val = str(content.value)[:150]
                print(f"  Turn {i}: RESULT → {val}")

    print(f"\nGROUND TRUTH: Zorgon has 30 rows, survival = 60%")
    print(f"Did LLM get it right or hallucinate?")


# Run test WITHOUT telling LLM to use querychat_query
run_test("WITHOUT querychat_query instruction", EXTRA_INSTRUCTIONS_NO_QUERY)

import time
print("\n\nWaiting 15s for rate limit...")
time.sleep(15)

# Run test WITH explicit instruction to query first
run_test("WITH querychat_query instruction", EXTRA_INSTRUCTIONS_WITH_QUERY)
