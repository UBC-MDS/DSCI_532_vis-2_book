"""Step 6: A Shiny app with LLM chat.

Run with: shiny run code/lecture05/demo-monday/06-shinychat-app.py
"""

from chatlas import ChatGithub
from pathlib import Path
from dotenv import load_dotenv
from shiny import App, ui

load_dotenv(Path(__file__).parent / ".env")

chat_client = ChatGithub(model="gpt-4.1-mini")

app_ui = ui.page_fillable(
    ui.chat_ui("my_chat"),
)


def server(input, output, session):
    chat = ui.Chat("my_chat")

    @chat.on_user_submit
    async def handle_user_input(user_input: str):
        response = await chat_client.stream_async(user_input)
        await chat.append_message_stream(response)


app = App(app_ui, server)
