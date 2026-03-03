"""Step 5: Switching providers — only the constructor changes.

Uncomment the provider you want to try.
Each requires the matching API key in .env:
  - GitHub Models: GITHUB_TOKEN
  - Anthropic: ANTHROPIC_API_KEY
  - OpenAI: OPENAI_API_KEY
"""

from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# --- GitHub Models (free) ---
from chatlas import ChatGithub
chat = ChatGithub(model="gpt-4.1")

# --- Anthropic (paid) ---
# from chatlas import ChatAnthropic
# chat = ChatAnthropic(model="claude-sonnet-4-0")

# --- OpenAI (paid) ---
# from chatlas import ChatOpenAI
# chat = ChatOpenAI(model="gpt-4.1")

# --- Ollama (free, local) ---
# from chatlas import ChatOllama
# chat = ChatOllama(model="qwen3:0.6b")

# Everything below works the same regardless of provider:
chat.chat("What is the capital of the moon?")
chat.chat("Are you sure?")
