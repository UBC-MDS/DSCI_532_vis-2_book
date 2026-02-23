import pandas as pd
import altair as alt
from vega_datasets import data as vega_data
from shiny import App, ui, render, reactive, req
from shinywidgets import output_widget, render_altair

cars = pd.DataFrame(vega_data.cars())
origins = sorted(cars["Origin"].unique())
display_cols = ["Name", "Miles_per_Gallon", "Cylinders", "Horsepower", "Origin"]

app_ui = ui.page_fluid(
    ui.h4("Cars explorer"),
    ui.input_select("origin", "Origin", choices=["All"] + origins),
    ui.layout_columns(
        ui.card(
            ui.card_header("Data — select rows to highlight"),
            ui.output_data_frame("tbl"),
        ),
        ui.card(
            ui.card_header("MPG vs Horsepower"),
            output_widget("scatter"),
        ),
        col_widths=[5, 7],
    ),
)

def server(input, output, session):

    @reactive.calc
    def filtered():
        df = cars[display_cols]
        if input.origin() != "All":
            df = df[cars["Origin"] == input.origin()]
        return df

    @render.data_frame
    def tbl():
        return render.DataGrid(filtered(), selection_mode="rows", height="300px")

    @render_altair
    def scatter():
        df = filtered()
        selected = tbl.data_view(selected=True)
        base = alt.Chart(df).mark_circle(color="#D1D5DB", size=60).encode(
            x="Miles_per_Gallon:Q", y="Horsepower:Q",
            tooltip=display_cols,
        )
        if selected.empty:
            return base.properties(width="container", height=320)
        hi = alt.Chart(selected).mark_circle(color="#3B82F6", size=90).encode(
            x="Miles_per_Gallon:Q", y="Horsepower:Q",
        )
        return (base + hi).properties(width="container", height=320)

app = App(app_ui, server)
