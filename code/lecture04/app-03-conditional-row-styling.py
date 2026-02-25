import pandas as pd
from vega_datasets import data as vega_data
from shiny import App, ui, render

# Sample rows spanning the full MPG range so all highlight bands appear
_all = pd.DataFrame(vega_data.cars())[["Name", "Miles_per_Gallon", "Horsepower", "Origin"]]
cars = pd.concat([
    _all[_all["Miles_per_Gallon"] >= 30].head(3),   # high MPG
    _all[_all["Miles_per_Gallon"].between(16, 25)].head(4),  # mid MPG (no highlight)
    _all[_all["Miles_per_Gallon"].between(25, 30)].head(2),  # borderline
    _all[_all["Miles_per_Gallon"] <= 15].head(3),   # low MPG
]).reset_index(drop=True)

# Colorblind-friendly palette (pastel Okabe-Ito)
COLOR_HIGH = "#D4E6F1"    # blue  — good (high MPG)
COLOR_LOW = "#F5CBA7"     # orange — bad (low MPG)
COLOR_BORDER = "#FCF3CF"  # yellow — borderline


def make_styles(df):
    styles = []
    for i, row in df.iterrows():
        mpg = row["Miles_per_Gallon"]
        if pd.isna(mpg):
            continue
        if mpg >= 30:
            styles.append({"rows": [i], "style": {"background-color": COLOR_HIGH}})
        elif mpg <= 15:
            styles.append({"rows": [i], "style": {"background-color": COLOR_LOW}})
        elif mpg >= 25:
            styles.append({"rows": [i], "style": {"background-color": COLOR_BORDER}})
    return styles


app_ui = ui.page_fluid(
    ui.h4("Row highlight: blue ≥ 30 MPG, yellow 25–30, orange ≤ 15 MPG"),
    ui.output_data_frame("tbl"),
)


def server(input, output, session):
    @render.data_frame
    def tbl():
        return render.DataGrid(cars, styles=make_styles(cars), width="100%")


app = App(app_ui, server)
