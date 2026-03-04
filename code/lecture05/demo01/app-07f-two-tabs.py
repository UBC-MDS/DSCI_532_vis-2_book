"""Step 7f: Two interfaces to the same data.

Tab 1 — LLM Chat: querychat natural-language filtering.
Tab 2 — Traditional: explicit filters + reactive calcs + Altair charts.

Run with: shiny run code/lecture05/demo-monday/app-07f-two-tabs.py
"""

from pathlib import Path

import altair as alt
import querychat
from chatlas import ChatGithub
from dotenv import load_dotenv
from seaborn import load_dataset
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_altair

load_dotenv(Path(__file__).parent / ".env")

# ── data ──────────────────────────────────────────────────────────────────────
titanic = load_dataset("titanic").dropna(subset=["age"])

# ── querychat (Tab 1) ─────────────────────────────────────────────────────────
qc = querychat.QueryChat(
    titanic.copy(),
    "titanic",
    greeting="""👋 Ask me anything about the Titanic passengers.

* <span class="suggestion">Show only survivors</span>
* <span class="suggestion">Filter to women in first class</span>
* <span class="suggestion">Who paid the highest fare?</span>
* <span class="suggestion">How many children were aboard?</span>
""",
    data_description="""
Titanic passenger manifest (714 passengers with known age).
- survived: 1=survived, 0=died
- pclass: 1=First (luxury), 2=Second, 3=Third (steerage)
- sex: 'male' or 'female'
- age: age in years
- fare: ticket price in pounds
- alone: True if travelling without family
- who: 'man', 'woman', or 'child' (under 16)
""",
    client=ChatGithub(model="gpt-4.1-mini"),
)

# ── UI ────────────────────────────────────────────────────────────────────────
app_ui = ui.page_navbar(
    # ── Tab 1: LLM Chat ───────────────────────────────────────────────────────
    ui.nav_panel(
        "LLM Chat",
        ui.layout_sidebar(
            qc.sidebar(),
            ui.card(
                ui.card_header(ui.output_text("chat_title")),
                ui.output_data_frame("chat_table"),
                fill=True,
            ),
            fillable=True,
        ),
    ),
    # ── Tab 2: Traditional Dashboard ─────────────────────────────────────────
    ui.nav_panel(
        "Traditional",
        ui.layout_column_wrap(
            ui.input_select(
                "pclass",
                "Class",
                choices={
                    "All": "All classes",
                    "1": "First",
                    "2": "Second",
                    "3": "Third",
                },
            ),
            ui.input_select(
                "sex",
                "Sex",
                choices={"All": "All", "male": "Male", "female": "Female"},
            ),
            ui.input_select(
                "survived",
                "Survived",
                choices={"All": "All", "1": "Yes", "0": "No"},
            ),
            ui.input_slider("age", "Age range", min=0, max=80, value=[0, 80]),
            width=1 / 4,
        ),
        ui.layout_column_wrap(
            ui.card(
                ui.card_header("Filtered passengers"),
                ui.output_data_frame("filtered_table"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Survival rate by class & sex"),
                ui.output_data_frame("agg_table"),
                full_screen=True,
            ),
            width=1 / 2,
        ),
        ui.layout_column_wrap(
            ui.card(
                ui.card_header("Survival count by class"),
                output_widget("chart_survival"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Age distribution by survival"),
                output_widget("chart_age"),
                full_screen=True,
            ),
            width=1 / 2,
        ),
    ),
    title="Titanic: Two Interfaces",
    fillable=True,
)


# ── Server ────────────────────────────────────────────────────────────────────
def server(input, output, session):

    # ── Tab 1: querychat ──────────────────────────────────────────────────────
    qc_vals = qc.server()

    @render.text
    def chat_title():
        return qc_vals.title() or "Titanic dataset"

    @render.data_frame
    def chat_table():
        return qc_vals.df()

    # ── Tab 2: reactive calcs ─────────────────────────────────────────────────
    @reactive.calc
    def filtered_df():
        df = titanic.copy()
        if input.pclass() != "All":
            df = df[df["pclass"] == int(input.pclass())]
        if input.sex() != "All":
            df = df[df["sex"] == input.sex()]
        if input.survived() != "All":
            df = df[df["survived"] == int(input.survived())]
        age_min, age_max = input.age()
        df = df[(df["age"] >= age_min) & (df["age"] <= age_max)]
        return df

    @reactive.calc
    def agg_df():
        df = filtered_df()
        return (
            df.groupby(["pclass", "sex"])
            .agg(
                passengers=("survived", "count"),
                survivors=("survived", "sum"),
            )
            .assign(
                survival_rate=lambda d: (d["survivors"] / d["passengers"] * 100).round(
                    1
                )
            )
            .reset_index()
            .rename(
                columns={
                    "pclass": "Class",
                    "sex": "Sex",
                    "passengers": "Passengers",
                    "survivors": "Survivors",
                    "survival_rate": "Survival Rate (%)",
                }
            )
        )

    @render.data_frame
    def filtered_table():
        return filtered_df()[["pclass", "sex", "age", "fare", "survived", "alone"]]

    @render.data_frame
    def agg_table():
        return agg_df()

    # ── Chart 1: survival count by class (grouped bar) ────────────────────────
    @render_altair
    def chart_survival():
        df = filtered_df()[["pclass", "survived"]].copy()
        df["survived_label"] = df["survived"].map({1: "Survived", 0: "Died"})
        df["pclass_label"] = df["pclass"].map({1: "First", 2: "Second", 3: "Third"})
        return (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X(
                    "pclass_label:N", title="Class", sort=["First", "Second", "Third"]
                ),
                y=alt.Y("count():Q", title="Passengers"),
                color=alt.Color(
                    "survived_label:N",
                    title="Status",
                    scale=alt.Scale(
                        domain=["Survived", "Died"], range=["#2ecc71", "#e74c3c"]
                    ),
                ),
                xOffset="survived_label:N",
                tooltip=["pclass_label", "survived_label", "count()"],
            )
            .properties(height=280)
        )

    # ── Chart 2: age distribution by survival (overlapping histogram) ─────────
    @render_altair
    def chart_age():
        df = filtered_df()[["age", "survived"]].copy()
        df["survived_label"] = df["survived"].map({1: "Survived", 0: "Died"})
        return (
            alt.Chart(df)
            .mark_bar(opacity=0.6)
            .encode(
                x=alt.X("age:Q", bin=alt.Bin(maxbins=20), title="Age"),
                y=alt.Y("count():Q", title="Passengers", stack=None),
                color=alt.Color(
                    "survived_label:N",
                    title="Status",
                    scale=alt.Scale(
                        domain=["Survived", "Died"], range=["#2ecc71", "#e74c3c"]
                    ),
                ),
                tooltip=["survived_label", "count()"],
            )
            .properties(height=280)
        )


app = App(app_ui, server)
