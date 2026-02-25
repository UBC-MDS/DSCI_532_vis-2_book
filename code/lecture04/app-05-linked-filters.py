import pandas as pd
from vega_datasets import data as vega_data
from shiny import App, ui, render, reactive, req

cars = pd.DataFrame(vega_data.cars())
origins = sorted(cars["Origin"].unique())
display_cols = ["Name", "Miles_per_Gallon", "Cylinders", "Horsepower", "Origin"]

app_ui = ui.page_fluid(
    ui.h4("Linked filters: origin → MPG slider range"),
    ui.layout_columns(
        ui.input_select("origin", "Origin", choices=["All"] + origins),
        ui.output_ui("mpg_slider"),   # placeholder — slider is built reactively
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

    @render.ui
    def mpg_slider():
        # Slider range is computed from the currently visible data — not the whole dataset.
        # When origin changes, this slider re-renders with an updated range.
        mpg_vals = filtered_by_origin()["Miles_per_Gallon"].dropna()
        if mpg_vals.empty:
            return ui.p("No MPG data.", class_="text-muted small")
        lo, hi = int(mpg_vals.min()), int(mpg_vals.max())
        return ui.input_slider("mpg", f"Min MPG ({lo}–{hi})", min=lo, max=hi, value=lo)

    @render.data_frame
    def tbl():
        req(input.mpg)   # wait for the dynamic slider to exist before reading it
        df = filtered_by_origin().dropna(subset=["Miles_per_Gallon"])
        df = df[df["Miles_per_Gallon"] >= input.mpg()]
        return render.DataGrid(df[display_cols].reset_index(drop=True), height="350px")


app = App(app_ui, server)
