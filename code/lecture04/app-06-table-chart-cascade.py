import pandas as pd
import altair as alt
from vega_datasets import data as vega_data
from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_altair

# Cascade pattern: table row selection → chart highlight
# Key: tbl.data_view(selected=True) returns the selected rows as a DataFrame,
# which drives a second Altair layer on top of the base scatter.

cars = pd.DataFrame(vega_data.cars())
origins = sorted(cars["Origin"].unique())
display_cols = ["Name", "Miles_per_Gallon", "Horsepower", "Cylinders", "Origin"]

app_ui = ui.page_fluid(
    ui.h4("Select rows in the table → highlighted in chart"),
    ui.p("Click rows (hold Shift for multiple). Chart updates immediately.",
         class_="text-muted small mb-3"),
    ui.input_select("origin", "Filter by origin", choices=["All"] + origins),
    ui.layout_columns(
        ui.card(
            ui.card_header("Data table — select rows"),
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
        df = cars.copy()
        if input.origin() != "All":
            df = df[df["Origin"] == input.origin()]
        return df[display_cols].reset_index(drop=True)

    @render.data_frame
    def tbl():
        return render.DataGrid(filtered(), selection_mode="rows", height="320px")

    @render_altair
    def scatter():
        df = filtered()
        # tbl.data_view(selected=True): currently selected rows as a DataFrame.
        # Returns empty DataFrame (not None) when nothing is selected.
        selected = tbl.data_view(selected=True)

        base = alt.Chart(df).mark_circle(size=60, opacity=0.5).encode(
            x=alt.X("Miles_per_Gallon:Q", title="Miles per Gallon"),
            y=alt.Y("Horsepower:Q", title="Horsepower"),
            color=alt.Color("Origin:N"),
            tooltip=display_cols,
        )

        if selected is None or selected.empty:
            return base.properties(width="container", height=300)

        # Selected rows rendered as a second layer: larger, full opacity, outlined
        highlight = alt.Chart(selected).mark_circle(
            size=200, opacity=1.0, stroke="black", strokeWidth=1.5,
        ).encode(
            x="Miles_per_Gallon:Q",
            y="Horsepower:Q",
            color=alt.Color("Origin:N"),
        )
        return (base + highlight).properties(width="container", height=300)


app = App(app_ui, server)
