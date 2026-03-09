"""Shiny Core app: ibis + DuckDB intro with penguins.

Shows the connect → build expression → .execute() lifecycle.
Run: shiny run app-01-ibis-intro.py
"""

import ibis
from ibis import _
from palmerpenguins import load_penguins
from shiny import App, reactive, render, ui

# -- Data setup (runs once at startup) ----------------------------------------

con = ibis.duckdb.connect()
penguins = con.create_table("penguins", load_penguins(), overwrite=True)

SPECIES = penguins.select("species").distinct().execute()["species"].tolist()

# -- UI -----------------------------------------------------------------------

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_selectize(
            "species",
            "Species",
            choices=SPECIES,
            selected=SPECIES,
            multiple=True,
        ),
        ui.input_selectize(
            "island",
            "Island",
            choices=penguins.select("island").distinct().execute()["island"].tolist(),
            selected=penguins.select("island").distinct().execute()["island"].tolist(),
            multiple=True,
        ),
    ),
    ui.output_text("count"),
    ui.output_data_frame("table"),
    title="Penguins — ibis + DuckDB",
)

# -- Server -------------------------------------------------------------------


def server(input, output, session):
    # Disconnect when the session ends — avoids connection leaks
    session.on_ended(con.disconnect)

    @reactive.calc
    def filtered():
        # Build the ibis expression — no query runs yet
        return penguins.filter(
            [
                _.species.isin(input.species()),
                _.island.isin(input.island()),
            ]
        )

    @render.text
    def count():
        # .count() is still lazy; .execute() triggers the DuckDB query
        n = filtered().count().execute()
        return f"{n:,} penguins match"

    @render.data_frame
    def table():
        return filtered().execute()


app = App(app_ui, server)
