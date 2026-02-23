import altair as alt
from shiny import App, ui
from shinywidgets import output_widget, render_altair

countries = alt.topo_feature(
    "https://vega.github.io/vega-datasets/data/world-110m.json",
    "countries",
)

app_ui = ui.page_fluid(
    ui.h4("Reactive map with projection selector"),
    ui.input_select(
        "projection",
        "Projection",
        choices=["equalEarth", "mercator", "orthographic"],
        selected="equalEarth",
    ),
    output_widget("map"),
)


def server(input, output, session):
    @output
    @render_altair
    def map():
        return (
            alt.Chart(countries)
            .mark_geoshape(stroke="white", strokeWidth=0.4)
            .encode(color=alt.value("#60A5FA"))
            .project(type=input.projection())
            .properties(height=430)
        )


app = App(app_ui, server)
