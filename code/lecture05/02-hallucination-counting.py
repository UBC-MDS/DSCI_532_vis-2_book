"""Step 2: Can LLMs count? Try different models."""

import json
import numpy as np
from chatlas import ChatGithub
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")


# OpenAI models support streaming; others on GitHub Models don't yet
OPENAI_MODELS = {"gpt-4.1", "gpt-4o", "gpt-4o-mini"}


def len_ai(n, model="gpt-4.1"):
    values = np.random.rand(n).tolist()
    chat = ChatGithub(model=model)
    stream = model in OPENAI_MODELS
    return chat.chat("How long is this array", json.dumps(values), stream=stream)


# Run these one at a time and observe:
print("--- n=10 ---")
len_ai(10)

print("\n--- n=100 ---")
len_ai(100)

print("\n--- n=1000 ---")
len_ai(1000)

print("\n--- n=10000 ---")
len_ai(10_000)

# Try switching models — all free on GitHub Models:
# print("\n--- n=10000, gpt-4o-mini ---")
# len_ai(10_000, model="gpt-4o-mini")        # smaller OpenAI model
#
# print("\n--- n=10000, Llama-3.3-70B-Instruct ---")
# len_ai(10_000, model="Llama-3.3-70B-Instruct")  # Meta open-source
#
# print("\n--- n=10000, Mistral-Small-2503 ---")
# len_ai(10_000, model="Mistral-Small-2503")  # Mistral small 3.1
#
# print("\n--- n=10000, Phi-4 ---")
# len_ai(10_000, model="Phi-4")               # Microsoft small model
#
# print("\n--- n=100, DeepSeek-R1 ---")
# len_ai(100, model="DeepSeek-R1")            # reasoning model (slow, 1 req/min)
