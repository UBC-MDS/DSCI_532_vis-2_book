import pandas as pd
from vega_datasets import data as vega_data
from shiny import App, ui, render

# Demonstrates the difference between tbl.data() and tbl.data_view():
#   tbl.data()         — always the full underlying DataFrame
#   tbl.data_view()    — what the user currently sees (honours column filters + sort)

cars = pd.DataFrame(vega_data.cars())
origins = sorted(cars["Origin"].unique())
display_cols = ["Name", "Miles_per_Gallon", "Horsepower", "Origin"]

app_ui = ui.page_fluid(
    ui.h4("Download: original data vs filtered view"),
    ui.input_select("origin", "Origin", choices=["All"] + origins),
    ui.layout_columns(
        ui.download_button("download_all",  "⬇ All data  (tbl.data())",          class_="btn-secondary"),
        ui.download_button("download_view", "⬇ Filtered view  (tbl.data_view())", class_="btn-primary"),
        col_widths=[6, 6],
    ),
    ui.output_text("counts"),
    ui.br(),
    ui.output_data_frame("tbl"),
)


def server(input, output, session):
    @render.data_frame
    def tbl():
        df = cars if input.origin() == "All" else cars[cars["Origin"] == input.origin()]
        return render.DataGrid(df[display_cols].reset_index(drop=True), height="300px")

    @render.text
    def counts():
        return (
            f"tbl.data(): {len(tbl.data())} rows (always full dataset)   |   "
            f"tbl.data_view(): {len(tbl.data_view())} rows (current filter)"
        )

    @render.download(filename="cars_all.csv")
    def download_all():
        # tbl.data() ignores any active filters or sort — returns full original data
        yield tbl.data().to_csv(index=False)

    @render.download(filename="cars_filtered.csv")
    def download_view():
        # tbl.data_view() respects column filters and sort order
        # Add selected=True to export only selected rows
        yield tbl.data_view().to_csv(index=False)


app = App(app_ui, server)
