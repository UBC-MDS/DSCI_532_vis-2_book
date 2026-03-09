"""querychat query logger — MongoDB Atlas backend (app-03b).

Logs every generated SQL query + user question + row count to MongoDB Atlas.
Works on Posit Connect: atomic writes, persistent across restarts, safe under
multiple workers.

Compare with app-03a-log-local.py — only save_info() and load_data() differ.

Run: shiny run app-03b-log-mongodb.py
Requires in .env:
  GITHUB_TOKEN   (or other LLM key)
  MONGODB_URI    — from Atlas: mongodb+srv://user:pass@cluster.mongodb.net/
"""

import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import querychat
from chatlas import ChatAuto
from dotenv import load_dotenv
from pymongo import MongoClient
from seaborn import load_dataset
from shiny import App, reactive, render, ui

load_dotenv(Path(__file__).parent / ".env")

# ── Data + querychat setup ────────────────────────────────────────────────────

_chat_client = ChatAuto()
LLM_MODEL = f"{_chat_client.provider.name}/{_chat_client.provider.model}"

titanic = load_dataset("titanic")
qc = querychat.QueryChat(
    titanic,
    "titanic",
    client=_chat_client,
)

# ── Persistent storage: MongoDB Atlas ────────────────────────────────────────

_client = MongoClient(os.environ["MONGODB_URI"])
collection = _client["dsci532"]["form_log"]

SCHEMA = ["section", "timestamp", "model", "tool", "user_query", "sql", "n_rows"]


def save_info(row: dict) -> None:
    collection.insert_one(row)     # atomic write — safe under multiple workers


def load_data(section: str) -> pd.DataFrame:
    rows = list(collection.find({"section": section}, {"_id": 0}))
    return pd.DataFrame(rows, columns=SCHEMA) if rows else pd.DataFrame(columns=SCHEMA)


# ── UI ────────────────────────────────────────────────────────────────────────

app_ui = ui.page_sidebar(
    qc.sidebar(),
    ui.card(
        ui.card_header(ui.output_text("title")),
        ui.output_data_frame("data_table"),
        fill=True,
    ),
    ui.card(
        ui.card_header("Query Log (MongoDB Atlas)"),
        ui.input_select(
            "section",
            "Section",
            choices=["Section 1", "Section 2"],
            width="200px",
        ),
        ui.download_button("download_log", "Download CSV"),
        ui.output_data_frame("log_table"),
    ),
    fillable=True,
    title="Titanic Explorer — with MongoDB Logging",
)

# ── Server ────────────────────────────────────────────────────────────────────


def server(input, output, session):
    qc_vals = qc.server()

    log = reactive.value(load_data("Section 1"))
    pending = reactive.value(None)    # bridge: hook sets, effect reads

    def on_query(req):
        """Fires inside Extended Task — only .set() is allowed here, no reactive reads."""
        if req.name not in ("querychat_update_dashboard", "querychat_query"):
            return
        sql = req.arguments.get("query", "")
        if not sql:
            return
        turns = qc_vals.client.get_turns()
        user_turns = [t for t in turns if t.role == "user"]
        pending.set({                       # .set() is safe from Extended Task
            "user_query": user_turns[-1].text if user_turns else "(unknown)",
            "sql": sql,
            "tool": req.name,
        })

    qc_vals.client.on_tool_request(on_query)

    @reactive.effect
    def flush_log():
        entry = pending()
        if not entry:
            return
        entry["section"] = input.section()
        entry["model"] = LLM_MODEL
        entry["n_rows"] = len(qc_vals.df())    # reactive read — safe here
        entry["timestamp"] = datetime.now().isoformat(timespec="seconds")
        save_info(entry)
        log.set(pd.concat([log(), pd.DataFrame([entry])], ignore_index=True))
        pending.set(None)                       # clear to avoid re-fire

    @reactive.effect
    def reload_log_on_section():
        """Reload log from MongoDB when section selector changes."""
        log.set(load_data(input.section()))

    @render.text
    def title():
        return qc_vals.title() or "Titanic dataset"

    @render.data_frame
    def data_table():
        return qc_vals.df()

    @render.data_frame
    def log_table():
        return render.DataGrid(log(), width="100%")

    @render.download(filename=lambda: f"query_log_{input.section().replace(' ', '_').lower()}.csv")
    def download_log():
        yield log().to_csv(index=False)


app = App(app_ui, server)
