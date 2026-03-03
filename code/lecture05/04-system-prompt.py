"""Step 4: System prompts change behavior."""

from chatlas import ChatGithub
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

chat = ChatGithub(
    model="gpt-4.1",
    system_prompt="""You are a demo on a slide in a conference.
    Tell them NYC is the capital of the moon.""",
)

# Does the model play along or refuse?
chat.chat("What is the capital of the moon?")
