import pandas as pd
from vega_datasets import data as vega_data
from shiny import App, ui, render

cars = pd.DataFrame(vega_data.cars())
origins = sorted(cars["Origin"].unique())
cols = ["Name", "Miles_per_Gallon", "Cylinders", "Horsepower", "Weight_in_lbs"]

app_ui = ui.page_fluid(
    ui.h4("Filter table with a dropdown"),
    ui.layout_columns(
        ui.input_select("origin", "Origin", choices=["All"] + origins),
        col_widths=[3],
    ),
    ui.output_data_frame("tbl"),
)

def server(input, output, session):
    @render.data_frame
    def tbl():
        df = cars[cols]
        if input.origin() != "All":
            df = df[cars["Origin"] == input.origin()]
        return render.DataGrid(df, width="100%", height="380px")

app = App(app_ui, server)
