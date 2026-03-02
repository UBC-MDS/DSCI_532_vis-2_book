"""Step 1: Verify your setup works."""

from chatlas import ChatGithub
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

chat = ChatGithub(model="gpt-4.1")
chat.chat("Say hello in one word.")
