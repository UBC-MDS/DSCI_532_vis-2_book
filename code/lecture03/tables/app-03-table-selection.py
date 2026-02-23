import pandas as pd
import altair as alt
from vega_datasets import data as vega_data
from shiny import App, ui, render, reactive, req
from shinywidgets import output_widget, render_altair

cars = pd.DataFrame(vega_data.cars()).iloc[:, :5]

app_ui = ui.page_fluid(
    ui.h4("Select rows to highlight them in the chart"),
    ui.layout_columns(
        ui.card(ui.output_data_frame("tbl"), height="300px"),
        ui.card(output_widget("scatter")),
        col_widths=[5, 7],
    ),
)

def server(input, output, session):
    @render.data_frame
    def tbl():
        return render.DataGrid(cars, selection_mode="rows", height="250px")

    @render_altair
    def scatter():
        selected = tbl.data_view(selected=True)
        base = alt.Chart(cars).mark_circle(color="#D1D5DB", size=60).encode(
            x=alt.X("Miles_per_Gallon:Q"),
            y=alt.Y("Horsepower:Q"),
            tooltip=["Name:N", "Miles_per_Gallon:Q", "Horsepower:Q"],
        )
        if selected.empty:
            return base.properties(width="container", height=260)
        highlight = alt.Chart(selected).mark_circle(color="#3B82F6", size=80).encode(
            x="Miles_per_Gallon:Q",
            y="Horsepower:Q",
        )
        return (base + highlight).properties(width="container", height=260)

app = App(app_ui, server)
