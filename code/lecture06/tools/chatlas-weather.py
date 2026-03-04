"""Tool calling demo: LLM looks up weather via two registered tools.

Run: cd code/lecture06/demo02 && python chatlas-weather.py
"""

import requests
from chatlas import ChatGithub
# from chatlas import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

from get_coordinates import get_coordinates
from get_weather import get_weather


chat = ChatGithub(
    model="gpt-4.1-mini",  # or "gpt-4.1"
    system_prompt=(
        "You are a helpful assistant that can check the weather. "
        "Report results in imperial units."
    ),
)

chat.register_tool(get_coordinates)
chat.register_tool(get_weather)

chat.chat("What is the weather in Seattle?")
