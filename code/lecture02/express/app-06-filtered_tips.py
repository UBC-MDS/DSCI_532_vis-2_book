import pandas as pd
import seaborn as sns
from shiny.express import input, render, ui


tips = sns.load_dataset("tips")

# title
ui.page_opts(title="Restaurant tipping", fillable=True)

# sidebar
with ui.sidebar(open="desktop"):
    ui.input_slider(
        id="slider",
        label="Bill amount",
        min=tips.total_bill.min(),
        max=tips.total_bill.max(),
        value=[tips.total_bill.min(), tips.total_bill.max()],
    )
    ui.input_checkbox_group(
        id="checkbox_group",
        label="Food service",
        choices={
            "Lunch": "Lunch",
            "Dinner": "Dinner",
        },
        selected=[
            "Lunch",
            "Dinner",
        ],
    )
    ui.input_action_button("action_button", "Reset filter")


# body of application

# first row of value boxes
with ui.layout_columns(fill=False):
    with ui.value_box():
        "Total tippers"

        @render.text
        def total_tippers():
            idx1 = tips.total_bill.between(
                left=input.slider()[0],
                right=input.slider()[1],
                inclusive="both",
            )
            idx2 = tips.time.isin(input.checkbox_group())
            tips_filtered = tips[idx1 & idx2]

            return tips_filtered.shape[0]
