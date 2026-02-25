import pandas as pd
from vega_datasets import data as vega_data
from shiny import App, ui, render, reactive, req

cars = pd.DataFrame(vega_data.cars())
origins = sorted(cars["Origin"].unique())
display_cols = ["Name", "Miles_per_Gallon", "Cylinders", "Horsepower", "Origin"]

# The slider is declared statically in the UI — not inside @render.ui.
app_ui = ui.page_fluid(
    ui.h4("Linked filters: update_slider approach"),
    ui.layout_columns(
        ui.input_select("origin", "Origin", choices=["All"] + origins),
        ui.input_slider("mpg", "Min MPG", min=0, max=50, value=0),
        col_widths=[6, 6],
    ),
    ui.output_data_frame("tbl"),
)


def server(input, output, session):
    @reactive.calc
    def filtered_by_origin():
        df = cars.copy()
        if input.origin() != "All":
            df = df[df["Origin"] == input.origin()]
        return df

    @reactive.effect
    def _update_mpg():
        mpg_vals = filtered_by_origin()["Miles_per_Gallon"].dropna()
        if mpg_vals.empty:
            return
        lo, hi = int(mpg_vals.min()), int(mpg_vals.max())
        ui.update_slider("mpg", label=f"Min MPG ({lo}–{hi})",
                         min=lo, max=hi, value=lo)

    @render.data_frame
    def tbl():
        df = filtered_by_origin().dropna(subset=["Miles_per_Gallon"])
        df = df[df["Miles_per_Gallon"] >= input.mpg()]
        return render.DataGrid(df[display_cols].reset_index(drop=True), height="350px")


app = App(app_ui, server)
