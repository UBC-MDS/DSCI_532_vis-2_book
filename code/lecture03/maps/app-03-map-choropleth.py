"""Year slider + projection selector -> life-expectancy choropleth.

Builds on app-02: adds a data-driven layer (choropleth via transform_lookup)
while keeping the projection selector from the previous example.
The slider filters gapminder rows; transform_lookup joins them to the
world TopoJSON for colouring.
"""

import altair as alt
import pandas as pd
from vega_datasets import data as vega_data
from shiny import App, ui
from shinywidgets import output_widget, render_altair

# ── data ────────────────────────────────────────────────────────────
# ISO 3166-1 numeric codes so gapminder rows match world-110m.json IDs
COUNTRY_IDS = {
    "Afghanistan": 4, "Argentina": 32, "Australia": 36, "Austria": 40,
    "Bangladesh": 50, "Belgium": 56, "Bolivia": 68, "Brazil": 76,
    "Canada": 124, "Chile": 152, "China": 156, "Colombia": 170,
    "Costa Rica": 188, "Croatia": 191, "Cuba": 192,
    "Dominican Republic": 214, "Ecuador": 218, "Egypt": 818,
    "El Salvador": 222, "Finland": 246, "France": 250, "Georgia": 268,
    "Germany": 276, "Greece": 300, "Haiti": 332, "Iceland": 352,
    "India": 356, "Indonesia": 360, "Iran": 364, "Iraq": 368,
    "Ireland": 372, "Israel": 376, "Italy": 380, "Jamaica": 388,
    "Japan": 392, "Kenya": 404, "Lebanon": 422, "Mexico": 484,
    "Netherlands": 528, "New Zealand": 554, "Nigeria": 566,
    "North Korea": 408, "Norway": 578, "Pakistan": 586, "Peru": 604,
    "Philippines": 608, "Poland": 616, "Portugal": 620, "Rwanda": 646,
    "Saudi Arabia": 682, "South Africa": 710, "South Korea": 410,
    "Spain": 724, "Switzerland": 756, "Turkey": 792,
    "United Kingdom": 826, "United States": 840, "Venezuela": 862,
}

gapminder = (
    pd.DataFrame(vega_data.gapminder())
    .assign(id=lambda df: df["country"].map(COUNTRY_IDS))
    .dropna(subset=["id"])
    .astype({"id": int})
)
countries_topo = alt.topo_feature(vega_data.world_110m.url, "countries")
years = sorted(gapminder["year"].unique())

app_ui = ui.page_fluid(
    ui.h4("Life expectancy over time"),
    ui.layout_columns(
        ui.input_slider(
            "year", "Year",
            min=min(years), max=max(years),
            value=max(years), step=5, sep="",
        ),
        ui.input_select(
            "projection", "Projection",
            choices=["equalEarth", "mercator", "naturalEarth1", "orthographic"],
            selected="equalEarth",
        ),
    ),
    output_widget("map"),
)


def server(input, output, session):
    @render_altair
    def map():
        yr = gapminder[gapminder["year"] == input.year()]
        proj = input.projection()

        # grey base layer — makes "no data" countries explicit rather than absent
        base = (
            alt.Chart(countries_topo)
            .mark_geoshape(fill="#d0d0d0", stroke="white", strokeWidth=0.35)
        )

        choropleth = (
            alt.Chart(countries_topo)
            .mark_geoshape(stroke="white", strokeWidth=0.35)
            .transform_lookup(
                lookup="id",
                from_=alt.LookupData(
                    yr, "id",
                    ["life_expect", "fertility", "pop", "country"],
                ),
            )
            .transform_filter("datum.life_expect !== null")
            .encode(
                color=alt.Color("life_expect:Q")
                    .scale(scheme="yellowgreenblue", domain=[20, 85])
                    .title("Life expectancy"),
                tooltip=[
                    alt.Tooltip("country:N", title="Country"),
                    alt.Tooltip("life_expect:Q", title="Life exp.", format=".1f"),
                    alt.Tooltip("fertility:Q", title="Fertility", format=".1f"),
                    alt.Tooltip("pop:Q", title="Population", format=","),
                ],
            )
        )

        return (
            alt.layer(base, choropleth)
            .project(type=proj)
            .properties(width=600, height=380)
        )


app = App(app_ui, server)
