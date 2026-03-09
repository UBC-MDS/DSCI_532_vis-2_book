## app-02a-taxi-inmem.py — ibis + DuckDB taxi dashboard (shinylive / in-memory version)
## Uses an embedded 400-row sample so it runs in the browser.
## For the full 3M-row version with lazy parquet loading: see app-02b-taxi-parquet.py

import random

import ibis
import pandas as pd
from ibis import _
from shiny import App, reactive, render, ui

# ── Embedded sample data (400 rows, realistic distributions) ─────────────────
random.seed(42)
_n = 400
_pw = [60, 30, 5, 5]
_vw = [45, 55]
_xw = [2, 70, 15, 6, 3, 2, 2]
_rows = []
for i in range(_n):
    d = round(random.uniform(0.1, 22), 1)
    f = round(2.5 + d * random.uniform(2.2, 3.5), 2)
    _rows.append(
        dict(
            VendorID=random.choices([1, 2], weights=_vw)[0],
            passenger_count=random.choices([0, 1, 2, 3, 4, 5, 6], weights=_xw)[0],
            trip_distance=d,
            payment_type=random.choices([1, 2, 3, 4], weights=_pw)[0],
            fare_amount=f,
            total_amount=round(f * random.uniform(1.05, 1.3), 2),
        )
    )

data = pd.DataFrame(_rows)

# In production this would be:
#   con = ibis.duckdb.connect()
#   taxi = con.read_parquet("data/taxi_2024-01.parquet")
taxi = ibis.memtable(data)

# ── UI ────────────────────────────────────────────────────────────────────────

PAYMENT_LABELS = {"1": "Credit card", "2": "Cash", "3": "No charge", "4": "Dispute"}
VENDOR_CHOICES = {"Both": "Both", "1": "Creative Mobile", "2": "VeriFone"}
PASSENGER_CHOICES = ["All", "0", "1", "2", "3"]

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_checkbox_group(
            "payment",
            "Payment type",
            choices=PAYMENT_LABELS,
            selected=list(PAYMENT_LABELS.keys()),
        ),
        ui.input_slider(
            "distance", "Trip distance (miles)", min=0, max=25, value=[0, 15], step=0.5
        ),
        ui.input_select(
            "passengers", "Passenger count", choices=PASSENGER_CHOICES, selected="All"
        ),
        ui.input_radio_buttons(
            "vendor", "Vendor", choices=VENDOR_CHOICES, selected="Both"
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
    title="NYC Taxi Sample — ibis + DuckDB",
)

# ── Server ────────────────────────────────────────────────────────────────────


def server(input, output, session):
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
            expr = expr.filter(_.passenger_count == int(input.passengers()))

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
            .select(["passenger_count", "trip_distance", "payment_type",
                     "fare_amount", "total_amount"])
            .execute()
        )


app = App(app_ui, server)
