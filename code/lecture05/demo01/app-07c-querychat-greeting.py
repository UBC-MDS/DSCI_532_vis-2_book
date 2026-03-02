"""Step 7c: Customize the greeting with clickable suggestion buttons.

Compare with 07-querychat-app.py — same app, different first impression.

Run with: shiny run code/lecture05/demo-monday/07c-querychat-greeting.py
"""

from pathlib import Path

import querychat
from chatlas import ChatGithub
from dotenv import load_dotenv
from seaborn import load_dataset
from shiny import App, render, ui

load_dotenv(Path(__file__).parent / ".env")

titanic = load_dataset("titanic")

GREETING = """
👋 Hi! I can help you explore the Titanic passenger data.

Try one of these to get started:

* <span class="suggestion">Show only passengers who survived</span>
* <span class="suggestion">Filter to first class women</span>
* <span class="suggestion">Who paid the highest fare?</span>
* <span class="suggestion">How many children were aboard?</span>
"""

qc = querychat.QueryChat(
    titanic,
    "titanic",
    greeting=GREETING,
    client=ChatGithub(model="gpt-4.1-mini"),
)

app_ui = ui.page_sidebar(
    qc.sidebar(),
    ui.card(
        ui.card_header(ui.output_text("title")),
        ui.output_data_frame("data_table"),
        fill=True,
    ),
    fillable=True,
    title="Titanic Explorer — Custom Greeting",
)


def server(input, output, session):
    qc_vals = qc.server()

    @render.text
    def title():
        return qc_vals.title() or "Titanic dataset"

    @render.data_frame
    def data_table():
        return qc_vals.df()


app = App(app_ui, server)
