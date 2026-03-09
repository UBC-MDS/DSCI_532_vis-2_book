"""NYC Yellow Taxi dashboard — ibis + DuckDB, lazy parquet loading (app-02b).

Reads ~3M trips from a local parquet file without loading it all into RAM.
Reactive inputs drive ibis expressions; .execute() fires DuckDB queries.

For the in-memory browser version (shinylive): see app-02a-taxi-inmem.py

Run: shiny run app-02b-taxi-parquet.py
Data: python prep_data.py  (run once first)
"""

from pathlib import Path

import ibis
from ibis import _
from shiny import App, reactive, render, ui

# -- Data setup (runs once at startup) ----------------------------------------

PARQUET = Path(__file__).parent / "data" / "taxi_2024-01.parquet"
if not PARQUET.exists():
    raise FileNotFoundError(
        "Missing taxi parquet file. Run `python prep_data.py` in code/lecture09 first."
    )

con = ibis.duckdb.connect()
taxi = con.read_parquet(str(PARQUET))  # table reference — no data loaded yet

PAYMENT_LABELS = {
    "1": "Credit card",
    "2": "Cash",
    "3": "No charge",
    "4": "Dispute",
}

VENDOR_CHOICES = {"Both": "Both", "1": "Creative Mobile", "2": "VeriFone"}
PASSENGER_CHOICES = ["All", "0", "1", "2", "3"]

# -- UI -----------------------------------------------------------------------

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_checkbox_group(
            "payment",
            "Payment type",
            choices=PAYMENT_LABELS,
            selected=list(PAYMENT_LABELS.keys()),
        ),
        ui.input_slider(
            "distance",
            "Trip distance (miles)",
            min=0,
            max=30,
            value=[0, 15],
            step=0.5,
        ),
        ui.input_select(
            "passengers",
            "Passenger count",
            choices=PASSENGER_CHOICES,
            selected="All",
        ),
        ui.input_radio_buttons(
            "vendor",
            "Vendor",
            choices=VENDOR_CHOICES,
            selected="Both",
        ),
        width=250,
    ),
    ui.layout_columns(
        ui.value_box("Matching trips", ui.output_text("n_trips")),
        ui.value_box("Avg fare", ui.output_text("avg_fare")),
        ui.value_box("Avg distance", ui.output_text("avg_dist")),
        col_widths=[4, 4, 4],
    ),
    ui.output_data_frame("table"),
    title="NYC Yellow Taxi — January 2024",
)

# -- Server -------------------------------------------------------------------


def server(input, output, session):
    session.on_ended(con.disconnect)

    @reactive.calc
    def filtered():
        expr = taxi

        if input.payment():
            expr = expr.filter(
                _.payment_type.isin([int(p) for p in input.payment()])
            )

        lo, hi = input.distance()
        expr = expr.filter(_.trip_distance.between(lo, hi))

        if input.passengers() != "All":
            expr = expr.filter(
                _.passenger_count == int(input.passengers())
            )

        if input.vendor() != "Both":
            expr = expr.filter(_.VendorID == int(input.vendor()))

        return expr

    @render.text
    def n_trips():
        return f"{filtered().count().execute():,}"

    @render.text
    def avg_fare():
        result = filtered().agg(avg=_.fare_amount.mean()).execute()
        return f"${result['avg'].iloc[0]:.2f}"

    @render.text
    def avg_dist():
        result = filtered().agg(avg=_.trip_distance.mean()).execute()
        return f"{result['avg'].iloc[0]:.1f} mi"

    @render.data_frame
    def table():
        return (
            filtered()
            .select(
                [
                    "tpep_pickup_datetime",
                    "passenger_count",
                    "trip_distance",
                    "payment_type",
                    "fare_amount",
                    "total_amount",
                ]
            )
            .limit(500)
            .execute()
        )


app = App(app_ui, server)
