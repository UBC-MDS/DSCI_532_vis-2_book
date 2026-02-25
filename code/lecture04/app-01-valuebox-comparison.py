import pandas as pd
from vega_datasets import data as vega_data
from shiny import App, ui, render, reactive
from faicons import icon_svg

cars = pd.DataFrame(vega_data.cars())
origins = sorted(cars["Origin"].unique())
BASELINE = {
    "mpg": cars["Miles_per_Gallon"].mean(),
    "hp": cars["Horsepower"].mean(),
    "accel": cars["Acceleration"].mean(),
}


def compare(current, baseline, higher_is_better=True):
    """
    Classify current vs baseline — five states:
      significantly above / slightly above / stable / slightly below / significantly below
    Thresholds:  change < 1%: stable, 1–5%: slight, > 5%: significant
    """
    # guard: can't compute a meaningful delta
    if baseline == 0 or pd.isna(current):
        return dict(icon="circle-minus", theme="secondary", badge="no data", label="no data")

    # percentage change relative to baseline; sign tells direction
    pct = (current - baseline) / abs(baseline) * 100

    # "good" depends on context: higher MPG is good, lower HP is good for efficiency
    is_good = (pct > 0) if higher_is_better else (pct < 0)
    abs_pct = abs(pct)

    # badge string shown below the value: e.g. "+5.6 (+24.3%) vs overall avg"
    sign = "+" if pct >= 0 else ""
    badge = f"{sign}{current - baseline:.1f} ({sign}{pct:.1f}%) vs overall avg"

    # under 1% change — treat as noise, no colour signal
    if abs_pct < 1:
        return dict(icon="arrow-right", theme="secondary", badge="≈ stable vs overall avg", label="stable")

    # direction: matching FA icon
    icon = "arrow-trend-up" if pct > 0 else "arrow-trend-down"

    # colour: good changes are green (success ≥5%, teal <5%),
    #         bad changes are red (danger ≥5%, warning <5%)
    theme = (
        "success" if (is_good and abs_pct >= 5) else
        "teal"    if is_good                    else
        "danger"  if abs_pct >= 5               else
        "warning"
    )

    quantifier = "significantly" if abs_pct >= 5 else "slightly"
    return dict(icon=icon, theme=theme, badge=badge,
                label=f"{quantifier} {'above' if pct > 0 else 'below'} avg")


def kpi_showcase(cmp):
    """FA icon sized for the value-box showcase panel — inherits theme colour."""
    # fill defaults to currentColor, so the icon matches the box's text colour
    # fill_opacity softens it slightly so it doesn't overpower the value
    return icon_svg(cmp["icon"], height="2.5em", fill_opacity="0.85")


def kpi_caption(cmp):
    """Delta badge + five-state label rendered below the value."""
    return ui.tags.div(
        # bold first line: absolute + relative delta, e.g. "+5.6 (+24.3%) vs overall avg"
        ui.HTML(f'<strong style="opacity:0.9">{cmp["badge"]}</strong>'),
        # dimmer second line: human-readable state, e.g. "significantly above avg"
        ui.div(cmp.get("label", ""), style="opacity:0.7;font-size:0.8rem;margin-top:2px"),
    )


app_ui = ui.page_fluid(
    ui.h5("Cars segment vs overall average"),
    ui.input_select("origin", "Origin", choices=["All"] + origins, selected="Japan"),
    ui.layout_column_wrap(
        ui.output_ui("mpg_box"),
        ui.output_ui("hp_box"),
        ui.output_ui("accel_box"),
        fill=False,
        width=1 / 3,
    ),
)


def server(input, output, session):
    @reactive.calc
    def seg():
        df = cars if input.origin() == "All" else cars[cars["Origin"] == input.origin()]
        return df.dropna(subset=["Miles_per_Gallon", "Horsepower", "Acceleration"])

    @render.ui  # higher MPG = better fuel economy ↑ green
    def mpg_box():
        val = seg()["Miles_per_Gallon"].mean()
        cmp = compare(val, BASELINE["mpg"], higher_is_better=True)
        return ui.value_box(
            "Mean MPG", f"{val:.1f}", kpi_caption(cmp),
            showcase=kpi_showcase(cmp),
            theme=cmp["theme"],
        )

    @render.ui  # lower HP = better efficiency ↓ green
    def hp_box():
        val = seg()["Horsepower"].mean()
        cmp = compare(val, BASELINE["hp"], higher_is_better=False)
        return ui.value_box(
            "Mean Horsepower", f"{val:.0f}", kpi_caption(cmp),
            showcase=kpi_showcase(cmp),
            theme=cmp["theme"],
        )

    @render.ui  # lower seconds = faster ↓ green; tends to be near-neutral across origins
    def accel_box():
        val = seg()["Acceleration"].mean()
        cmp = compare(val, BASELINE["accel"], higher_is_better=False)
        return ui.value_box(
            "Mean Acceleration (s)", f"{val:.1f}", kpi_caption(cmp),
            showcase=kpi_showcase(cmp),
            theme=cmp["theme"],
        )


app = App(app_ui, server)
