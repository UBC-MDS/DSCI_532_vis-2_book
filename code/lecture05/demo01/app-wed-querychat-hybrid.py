"""Step 7b: Shiny controls + querychat together (Pattern A).

A pclass dropdown sets a SQL filter on querychat. The chat can refine further.
Both the dropdown and the chat share the same reactive filter state.

Run with: shiny run code/lecture05/demo-monday/07b-querychat-hybrid.py
"""

from pathlib import Path

import querychat
from chatlas import ChatGithub
from dotenv import load_dotenv
from seaborn import load_dataset
from shiny import App, reactive, render, ui

load_dotenv(Path(__file__).parent / ".env")

titanic = load_dataset("titanic")

qc = querychat.QueryChat(
    titanic,
    "titanic",
    client=ChatGithub(model="gpt-4.1-mini"),
)

app_ui = ui.page_sidebar(
    qc.sidebar(),
    ui.card(
        ui.card_header(
            ui.input_select(
                "pclass",
                "Passenger class:",
                choices={"All": "All classes", "1": "1st", "2": "2nd", "3": "3rd"},
            )
        ),
        ui.output_data_frame("data_table"),
        fill=True,
    ),
    fillable=True,
    title="Titanic Explorer (Hybrid)",
)


def server(input, output, session):
    qc_vals = qc.server()

    # Shiny input drives the SQL filter on querychat
    @reactive.effect
    def sync_dropdown():
        pclass = input.pclass()
        if pclass == "All":
            qc_vals.sql.set(None)
            qc_vals.title.set(None)
        else:
            qc_vals.sql.set(f"SELECT * FROM titanic WHERE pclass = {pclass}")
            qc_vals.title.set(f"{pclass}st/nd/rd class passengers")

    @render.data_frame
    def data_table():
        return qc_vals.df()


app = App(app_ui, server)
