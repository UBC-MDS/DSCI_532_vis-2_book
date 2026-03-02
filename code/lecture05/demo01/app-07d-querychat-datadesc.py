"""Step 7d: Add data_description so the LLM understands column semantics.

Without it, the LLM only sees column names and types — not what they mean.
Compare: ask "show children" with vs without data_description.

Run with: shiny run code/lecture05/demo-monday/07d-querychat-datadesc.py
"""

from pathlib import Path

import querychat
from chatlas import ChatGithub
from dotenv import load_dotenv
from seaborn import load_dataset
from shiny import App, render, ui

load_dotenv(Path(__file__).parent / ".env")

titanic = load_dataset("titanic")

DATA_DESCRIPTION = """
Titanic passenger manifest (891 passengers).

Column meanings:
- survived: 1 = survived, 0 = died
- pclass: ticket class — 1 = First (luxury), 2 = Second, 3 = Third (steerage)
- sex: passenger sex ('male' or 'female')
- age: age in years (some missing)
- sibsp: number of siblings or spouses aboard
- parch: number of parents or children aboard
- fare: ticket price in pounds sterling
- embarked: port of embarkation — C = Cherbourg, Q = Queenstown, S = Southampton
- who: 'man', 'woman', or 'child' (child = under 16)
- alone: True if travelling alone (sibsp=0 and parch=0)
- alive: 'yes' or 'no' (same as survived, string version)
- deck: cabin deck (A–G), many missing
"""

qc = querychat.QueryChat(
    titanic,
    "titanic",
    data_description=DATA_DESCRIPTION,
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
    title="Titanic Explorer — Data Description",
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
