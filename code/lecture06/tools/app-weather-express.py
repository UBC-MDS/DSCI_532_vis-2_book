"""Shiny Express app: weather chatbot with tool calling.

Run: shiny run app-weather-express.py
"""

from chatlas import ChatGithub
# from chatlas import ChatAnthropic
from dotenv import load_dotenv
from shiny.express import ui

load_dotenv()

from get_coordinates import get_coordinates
from get_weather import get_weather

chat_client = ChatGithub(model="gpt-4.1-mini")
# chat_client = ChatGithub(model="gpt-4.1")
# chat_client = ChatAnthropic()

chat_client.register_tool(get_coordinates)
chat_client.register_tool(get_weather)

chat = ui.Chat(id="chat")
chat.ui(
    messages=[
        "Hello! I am a weather bot! Where would you like to get the weather for?"
    ]
)


@chat.on_user_submit
async def _(user_input: str):
    response = await chat_client.stream_async(user_input, content="all")
    await chat.append_message_stream(response)
