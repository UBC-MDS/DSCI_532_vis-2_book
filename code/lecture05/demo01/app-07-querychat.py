"""Step 7: LLM-powered data filtering with querychat.

Run with: shiny run code/lecture05/demo-monday/07-querychat-app.py

Ask it: "Show only women who survived" or "filter to first class passengers"
"""

from pathlib import Path

import querychat
from chatlas import ChatGithub
from dotenv import load_dotenv
from seaborn import load_dataset
from shiny import App, render, ui

# Load .env from the same directory as this script, regardless of CWD
load_dotenv(Path(__file__).parent / ".env")

# data -----
titanic = load_dataset("titanic")

# querychat setup -----
qc = querychat.QueryChat(
    titanic,
    "titanic",
    client=ChatGithub(model="gpt-4.1-mini"),
)

# ui -----
app_ui = ui.page_sidebar(
    qc.sidebar(),
    ui.card(
        ui.card_header(ui.output_text("title")),
        ui.output_data_frame("data_table"),
        fill=True,
    ),
    fillable=True,
    title="Titanic Explorer",
)


# server -----
def server(input, output, session):
    qc_vals = qc.server()

    @render.text
    def title():
        return qc_vals.title() or "Titanic dataset"

    @render.data_frame
    def data_table():
        return qc_vals.df()


app = App(app_ui, server)
