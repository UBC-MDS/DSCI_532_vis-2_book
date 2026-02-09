from shiny import ui, render, App
import altair as alt
from palmerpenguins import load_penguins
from shinywidgets import render_altair, output_widget

dat = load_penguins().dropna()

app_ui = ui.page_fluid(
    ui.input_radio_buttons(
        id="species",
        label="Species",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        inline=True,
    ),
    output_widget("plot"),
)


def server(input, output, session):
    @render_altair
    def plot():
        dat = load_penguins().dropna()

        species = "Gentoo"  # selected species
        sel = dat.loc[dat.species == species]  # selected data

        # Base histogram for all data
        base = (
            alt.Chart(dat)
            .mark_bar(color="#C2C2C4", binSpacing=0)
            .encode(
                alt.X("bill_length_mm:Q", bin=alt.Bin(step=1), title="bill_length_mm"),
                alt.Y("count()", title="count"),
            )
        )

        # Overlay histogram for selected species
        overlay = (
            alt.Chart(sel)
            .mark_bar(color="#447099", binSpacing=0)
            .encode(alt.X("bill_length_mm:Q", bin=alt.Bin(step=1)), alt.Y("count()"))
        )

        return base + overlay


app = App(app_ui, server)
