"""Step 3: Your first chat conversation."""

from chatlas import ChatGithub
from pathlib import Path
from dotenv import load_dotenv

try:
    load_dotenv(Path(__file__).parent / ".env")
except NameError:
    load_dotenv()
    load_dotenv(Path("code/lecture05/demo01/.env"))

chat = ChatGithub(
    model="gpt-4.1",
    system_prompt="You are a terse assistant.",
)

# First question
chat.chat("What is the capital of the moon?")

# Follow-up (chat object remembers history)
chat.chat("Are you sure?")
