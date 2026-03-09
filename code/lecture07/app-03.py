"""MongoDB write patterns: feedback form + editable DataGrid (app-03).

Demonstrates two ways to write user data to MongoDB Atlas from a Shiny app:
  1. Simple feedback form — text inputs + button → insert_one
  2. Editable DataGrid — inline editing + submit → insert_one per row

Run: shiny run app-03.py
Requires in .env:
  MONGODB_URI  — from Atlas: mongodb+srv://user:pass@cluster.mongodb.net/
"""

import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from shiny import App, reactive, render, ui

load_dotenv(Path(__file__).parent / ".env")

# ── MongoDB setup ─────────────────────────────────────────────────────────────

_client = MongoClient(os.environ["MONGODB_URI"])
collection = _client["dsci532"]["form_log"]

# ── Editable DataGrid template ────────────────────────────────────────────────

template_df = pd.DataFrame({
    "name":    [""] * 3,
    "species": [""] * 3,
    "island":  [""] * 3,
    "comment": [""] * 3,
})

# ── UI ────────────────────────────────────────────────────────────────────────

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h5("Feedback form"),
        ui.input_text("name", "Your name"),
        ui.input_text_area("comment", "Comment"),
        ui.input_action_button("submit", "Submit", class_="btn-primary w-100"),
    ),
    ui.tags.style("""
        .shiny-data-grid tr { height: 42px; }
        .shiny-data-grid td { padding: 8px 12px; vertical-align: middle; }
    """),
    ui.h4("Editable DataGrid → MongoDB"),
    ui.p("Edit the table below, then click Submit Rows."),
    ui.output_data_frame("response_table"),
    ui.input_action_button("submit_grid", "Submit Rows", class_="btn-secondary mt-2"),
    ui.hr(),
    ui.h4("Submissions log"),
    ui.output_data_frame("log_table"),
    title="App 03 — MongoDB write patterns",
)

# ── Server ────────────────────────────────────────────────────────────────────


def server(input, output, session):

    # Pattern 1: form → insert_one on button click
    @reactive.effect
    @reactive.event(input.submit)
    def save_response():
        row = {
            "source":    "form",
            "name":      input.name(),
            "comment":   input.comment(),
            "timestamp": datetime.now().isoformat(),
        }
        collection.insert_one(row)
        ui.notification_show("Submitted!", type="message", duration=3)

    # Pattern 2: editable DataGrid → insert_one per row on button click
    @render.data_frame
    def response_table():
        return render.DataGrid(template_df, editable=True, height="200px")

    @reactive.effect
    @reactive.event(input.submit_grid)
    def save_edits():
        edited = response_table.data_view()
        filled = edited[edited["name"].str.strip() != ""]
        for row in filled.to_dict("records"):
            row["source"] = "grid"
            row["timestamp"] = datetime.now().isoformat()
            collection.insert_one(row)
        ui.notification_show(f"{len(filled)} row(s) submitted!", type="message", duration=3)

    # Live log viewer
    @render.data_frame
    @reactive.event(input.submit, input.submit_grid)
    def log_table():
        rows = list(collection.find({}, {"_id": 0}))
        return pd.DataFrame(rows) if rows else pd.DataFrame()


app = App(app_ui, server)
