import pandas as pd
import altair as alt
from vega_datasets import data as vega_data
from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_altair
from faicons import icon_svg

cars = pd.DataFrame(vega_data.cars())
origins = sorted(cars["Origin"].unique())
display_cols = ["Name", "Miles_per_Gallon", "Cylinders", "Horsepower", "Origin"]
BASELINE = {
    "mpg": cars["Miles_per_Gallon"].mean(),
    "hp": cars["Horsepower"].mean(),
}


def compare(current, baseline, higher_is_better=True):
    if baseline == 0 or pd.isna(current):
        return dict(icon="circle-minus", theme="secondary", badge="no data")
    pct = (current - baseline) / abs(baseline) * 100
    is_good = (pct > 0) if higher_is_better else (pct < 0)
    abs_pct = abs(pct)
    sign = "+" if pct >= 0 else ""
    badge = f"{sign}{pct:.1f}% vs avg"
    if abs_pct < 1:
        return dict(icon="arrow-right", theme="secondary", badge="≈ avg")
    icon = "arrow-trend-up" if pct > 0 else "arrow-trend-down"
    theme = (
        "success" if (is_good and abs_pct >= 5) else
        "teal"    if is_good                    else
        "danger"  if abs_pct >= 5               else
        "warning"
    )
    return dict(icon=icon, theme=theme, badge=badge)


# Header: bg-primary is theme-aware; d-flex pushes badge to the right
header = ui.div(
    ui.div(
        ui.h2("Cars Explorer", class_="mb-0 fs-4"),
        ui.p("Fuel economy dataset · 1970–1982", class_="mb-0 opacity-75 small"),
    ),
    ui.tags.span("v1.0", class_="badge bg-light text-dark"),
    class_="bg-primary text-white p-3 d-flex justify-content-between align-items-center",
)

sidebar = ui.sidebar(
    ui.h6("Filters"),
    ui.input_select("origin", "Origin", choices=["All"] + origins),
    ui.hr(),
    ui.p("Select rows in the table to highlight in the chart.",
         style="font-size:0.8rem; color:#6B7280;"),
    width=200,
)

app_ui = ui.page_fluid(
    header,
    ui.layout_sidebar(
        sidebar,
        ui.layout_column_wrap(
            ui.output_ui("n_rows_box"),
            ui.output_ui("mpg_box"),
            ui.output_ui("hp_box"),
            fill=False,
            width=1 / 3,
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Data"),
                ui.output_data_frame("tbl"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("MPG vs Horsepower"),
                output_widget("scatter"),
                full_screen=True,
            ),
            col_widths=[5, 7],
        ),
    ),
)


def server(input, output, session):
    @reactive.calc
    def filtered():
        df = cars.copy()
        if input.origin() != "All":
            df = df[df["Origin"] == input.origin()]
        return df[display_cols].reset_index(drop=True)

    @render.ui
    def n_rows_box():
        n = len(filtered())
        total = len(cars)
        return ui.value_box(
            "Total rows", str(n), f"of {total}",
            showcase=icon_svg("table", height="2em"),
            theme="primary",
        )

    @render.ui
    def mpg_box():
        val = filtered()["Miles_per_Gallon"].mean()
        cmp = compare(val, BASELINE["mpg"], higher_is_better=True)
        return ui.value_box(
            "Mean MPG", f"{val:.1f}", cmp["badge"],
            showcase=icon_svg(cmp["icon"], height="2em"),
            theme=cmp["theme"],
        )

    @render.ui
    def hp_box():
        val = filtered()["Horsepower"].mean()
        cmp = compare(val, BASELINE["hp"], higher_is_better=False)
        return ui.value_box(
            "Mean HP", f"{val:.0f}", cmp["badge"],
            showcase=icon_svg(cmp["icon"], height="2em"),
            theme=cmp["theme"],
        )

    @render.data_frame
    def tbl():
        return render.DataGrid(filtered(), selection_mode="rows", height="350px")

    @render_altair
    def scatter():
        df = filtered()
        selected = tbl.data_view(selected=True)
        base = alt.Chart(df).mark_circle(color="#D1D5DB", size=60).encode(
            x="Miles_per_Gallon:Q", y="Horsepower:Q",
            tooltip=display_cols,
        )
        if selected is None or selected.empty:
            return base.properties(width="container", height=320)
        hi = alt.Chart(selected).mark_circle(color="#3B82F6", size=90).encode(
            x="Miles_per_Gallon:Q", y="Horsepower:Q",
        )
        return (base + hi).properties(width="container", height=320)


app = App(app_ui, server)
