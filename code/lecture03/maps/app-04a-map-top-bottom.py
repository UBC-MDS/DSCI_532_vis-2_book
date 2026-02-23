"""Region + year → map + top-5 / bottom-5 charts via @reactive.calc.

Demonstrates that a single @reactive.calc can feed THREE outputs:
  • a choropleth map
  • a bar chart of the 5 highest life-expectancy countries
  • a bar chart of the 5 lowest life-expectancy countries

The data is filtered only once; all three outputs share that result.
Countries and rankings shift as the year or region changes.
"""

import altair as alt
import pandas as pd
from vega_datasets import data as vega_data
from shiny import App, ui, reactive
from shinywidgets import output_widget, render_altair

# ── data ────────────────────────────────────────────────────────────
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

REGIONS = {
    "All": None,
    "Americas": [
        "Argentina", "Bolivia", "Brazil", "Canada", "Chile", "Colombia",
        "Costa Rica", "Cuba", "Dominican Republic", "Ecuador",
        "El Salvador", "Haiti", "Jamaica", "Mexico", "Peru",
        "United States", "Venezuela",
    ],
    "Europe": [
        "Austria", "Belgium", "Croatia", "Finland", "France", "Georgia",
        "Germany", "Greece", "Iceland", "Ireland", "Italy", "Netherlands",
        "Norway", "Poland", "Portugal", "Spain", "Switzerland", "Turkey",
        "United Kingdom",
    ],
    "Asia & Pacific": [
        "Afghanistan", "Australia", "Bangladesh", "China", "India",
        "Indonesia", "Japan", "New Zealand", "North Korea", "Pakistan",
        "Philippines", "South Korea",
    ],
    "Middle East & Africa": [
        "Egypt", "Iran", "Iraq", "Israel", "Kenya", "Lebanon",
        "Nigeria", "Rwanda", "Saudi Arabia", "South Africa",
    ],
}

gapminder = (
    pd.DataFrame(vega_data.gapminder())
    .assign(id=lambda df: df["country"].map(COUNTRY_IDS))
    .dropna(subset=["id"])
    .astype({"id": int})
)
countries_topo = alt.topo_feature(vega_data.world_110m.url, "countries")
years = sorted(gapminder["year"].unique())

# ── UI ──────────────────────────────────────────────────────────────
app_ui = ui.page_fluid(
    ui.h4("Gapminder explorer"),
    ui.layout_columns(
        ui.input_select("region", "Region", choices=list(REGIONS.keys())),
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
        col_widths=[3, 6, 3],
    ),
    ui.div(
        output_widget("map"),
        style="min-height: 480px;",
    ),
    ui.layout_columns(
        output_widget("top5"),
        output_widget("bottom5"),
        col_widths=[6, 6],
    ),
)


# ── helpers ─────────────────────────────────────────────────────────
def bar_chart(df, title):
    return (
        alt.Chart(df, title=title)
        .mark_bar()
        .encode(
            x=alt.X("life_expect:Q").scale(zero=True).title("Life expectancy"),
            y=alt.Y("country:N").sort("-x").title(None)
                .axis(alt.Axis(labelLimit=160, minExtent=140)),
            color=alt.Color("life_expect:Q")
                .scale(scheme="yellowgreenblue", domain=[20, 85])
                .legend(None),
            tooltip=[
                alt.Tooltip("country:N"),
                alt.Tooltip("life_expect:Q", title="Life exp.", format=".1f"),
            ],
        )
        .properties(width="container", height=160)
    )


# ── server ──────────────────────────────────────────────────────────
def server(input, output, session):

    @reactive.calc
    def filtered():
        """Filter once; top5, bottom5, and map all share this result."""
        df = gapminder[gapminder["year"] == input.year()]
        members = REGIONS[input.region()]
        if members is not None:
            df = df[df["country"].isin(members)]
        return df.sort_values("life_expect", ascending=False)

    @render_altair
    def map():
        df = filtered()

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
                    df, "id", ["life_expect", "country"],
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
                ],
            )
        )
        return (
            alt.layer(base, choropleth)
            .project(type=input.projection())
            .properties(width="container", height=450)
        )

    @render_altair
    def top5():
        df = filtered().head(5)
        return bar_chart(df, "Top 5 — highest life expectancy")

    @render_altair
    def bottom5():
        df = filtered().tail(5)
        return bar_chart(df, "Bottom 5 — lowest life expectancy")


app = App(app_ui, server)
