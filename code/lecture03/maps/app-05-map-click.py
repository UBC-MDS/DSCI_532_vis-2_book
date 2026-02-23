"""Client-side click interaction — no Shiny reactivity needed.

Clicking a country highlights it in blue and greys out the rest.
The entire interaction is handled by Altair's selection_point inside
the browser — the Shiny server is never involved.

Compare with apps 03/04 where inputs go to the server and trigger
a full re-render. Here the chart renders once and Vega-Lite handles
clicks locally.
"""

import altair as alt
import pandas as pd
from vega_datasets import data as vega_data
from shiny import App, ui
from shinywidgets import output_widget, render_altair

# Build a small id → name lookup from gapminder
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
country_names = pd.DataFrame(
    [{"id": v, "country": k} for k, v in COUNTRY_IDS.items()]
)

countries_topo = alt.topo_feature(vega_data.world_110m.url, "countries")

app_ui = ui.page_fluid(
    ui.h4("Click a country to highlight it"),
    ui.p(
        ui.tags.em("All interaction happens inside the chart — no server round-trip."),
        style="color: #6B7280; font-size: 0.9rem;",
    ),
    output_widget("world_map"),
)


def server(input, output, session):
    @render_altair
    def world_map():
        click = alt.selection_point(fields=["id"], empty=False)

        return (
            alt.Chart(countries_topo)
            .mark_geoshape(stroke="white", strokeWidth=0.5)
            .transform_lookup(
                lookup="id",
                from_=alt.LookupData(country_names, "id", ["country"]),
            )
            .encode(
                color=alt.condition(
                    click,
                    alt.value("#3B82F6"),   # highlighted
                    alt.value("#D1D5DB"),   # unselected
                ),
                tooltip=[
                    alt.Tooltip("country:N", title="Country"),
                    alt.Tooltip("id:Q", title="ISO numeric id"),
                ],
            )
            .project(type="equalEarth")
            .add_params(click)
            .properties(width="container", height=440)
        )


app = App(app_ui, server)
