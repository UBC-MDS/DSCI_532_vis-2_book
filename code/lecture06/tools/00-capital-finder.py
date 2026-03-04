"""Tool calling intro: register a simple tool that overrides the LLM's knowledge.

Callback to the moon/NYC example from lecture 7 — now solved with a tool
instead of a system prompt hack.

Key question: does registering a tool guarantee the model will use it?

Run: python 00-capital-finder.py
"""

from chatlas import ChatAnthropic, ChatGithub
from dotenv import load_dotenv

load_dotenv()


def capital_finder(location: str) -> str:
    """Look up the capital of a place. Returns the capital city name."""
    if "moon" in location.lower():
        return "NYC"
    return f"I don't know the capital of {location}"


# --- Attempt 1: no system prompt ------------------------------------------
# The model has the tool but decides on its own whether to call it.
# gpt-4.1-mini often answers from its own knowledge instead.
chat = ChatGithub(model="gpt-4.1-mini")
chat.register_tool(capital_finder)

print("── Without system prompt ───────────────────────────")
chat.chat("What is the capital of the moon?")

# --- Attempt 2: system prompt encourages tool use ------------------------
# Adding a system prompt that tells the model to ALWAYS use the tool.
chat2 = ChatGithub(
    model="gpt-4.1-mini",
    system_prompt=(
        "You are a geography assistant. "
        "IMPORTANT: For ANY question about a capital, you MUST call the "
        "capital_finder tool first — even if the location seems unusual. "
        "Never refuse or answer from your own knowledge. Call the tool, "
        "then report what it returns."
    ),
)
chat2.register_tool(capital_finder)

print("\n── With system prompt ──────────────────────────────")
chat2.chat("What is the capital of the moon?")

# --- Attempt 3: Anthropic without system prompt ---------------------------
chat3 = ChatAnthropic()
chat3.register_tool(capital_finder)

print("\n── Anthropic, without system prompt ────────────────")
chat3.chat("What is the capital of the moon?")

# --- Attempt 4: Anthropic with system prompt ------------------------------
chat4 = ChatAnthropic(
    system_prompt=(
        "You are a geography assistant. "
        "IMPORTANT: For ANY question about a capital, you MUST call the "
        "capital_finder tool first — even if the location seems unusual. "
        "Never refuse or answer from your own knowledge. Call the tool, "
        "then report what it returns."
    ),
)
chat4.register_tool(capital_finder)

print("\n── Anthropic, with system prompt ───────────────────")
chat4.chat("What is the capital of the moon?")
