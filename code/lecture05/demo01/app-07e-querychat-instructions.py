"""Step 7e: extra_instructions to shape LLM behaviour.

Instructs the model to always include survival context and suggest comparisons.

Run with: shiny run code/lecture05/demo-monday/07e-querychat-instructions.py
"""

from pathlib import Path

import querychat
from chatlas import ChatGithub
from dotenv import load_dotenv
from seaborn import load_dataset
from shiny import App, render, ui

load_dotenv(Path(__file__).parent / ".env")

titanic = load_dataset("titanic")

EXTRA_INSTRUCTIONS = """
When filtering the data, always reply using EXACTLY this format — no exceptions:

🎯 **Filter:** [one sentence describing what was selected]
📊 **Stats:** use querychat_query to calculate row count and survival rate, then write: [N rows] | survival rate: [X%] | overall: 38.4%
💡 **Insight:** [one sentence interpreting whether this group survived better or worse than average]
🔍 **Try next:** <span class="suggestion">[a natural follow-up question]</span>
"""

qc = querychat.QueryChat(
    titanic,
    "titanic",
    extra_instructions=EXTRA_INSTRUCTIONS,
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
    title="Titanic Explorer — Custom Instructions",
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
