import pandas as pd
from vega_datasets import data as vega_data
from shiny import App, ui, render, reactive

# Demonstrates programmatic selection reset:
# Changing the origin filter (or clicking Reset) forces filtered() to recompute,
# which re-renders the DataGrid — DataGrid automatically clears its selection
# whenever the underlying data reference changes.

cars = pd.DataFrame(vega_data.cars())
origins = sorted(cars["Origin"].unique())

app_ui = ui.page_fluid(
    ui.h4("Filter → selection resets automatically"),
    ui.layout_columns(
        ui.input_select("origin", "Origin", choices=["All"] + origins),
        ui.input_action_button("reset_btn", "Reset selection", class_="btn-secondary"),
        col_widths=[6, 6],
    ),
    ui.output_text("selection_info"),
    ui.br(),
    ui.output_data_frame("tbl"),
)


def server(input, output, session):
    @reactive.calc
    def filtered():
        # Take an explicit dependency on reset_btn so clicking it invalidates
        # filtered(), which in turn re-renders the DataGrid and clears the selection.
        _ = input.reset_btn()
        df = cars.copy()
        if input.origin() != "All":
            df = df[df["Origin"] == input.origin()]
        return df[["Name", "Miles_per_Gallon", "Cylinders", "Origin"]].reset_index(drop=True)

    @render.data_frame
    def tbl():
        return render.DataGrid(filtered(), height="350px", selection_mode="rows")

    @render.text
    def selection_info():
        selected = tbl.data_view(selected=True)
        n = 0 if (selected is None or selected.empty) else len(selected)
        return f"Selected rows: {n}  (changes filter or click Reset to clear)"


app = App(app_ui, server)
