from shiny import App, ui, render
from vega_datasets import data as vega_data
import pandas as pd

cars = pd.DataFrame(vega_data.cars()).iloc[:, :5]

app_ui = ui.page_fluid(
    ui.h4("Cars dataset"),
    ui.layout_columns(
        ui.input_switch("filters", "Show filters", True),
        col_widths=[3],
    ),
    ui.output_data_frame("grid"),
)

def server(input, output, session):
    @render.data_frame
    def grid():
        return render.DataGrid(
            cars,
            filters=input.filters(),
            height="400px",
            width="100%",
        )

app = App(app_ui, server)
