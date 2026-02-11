import pandas as pd
import seaborn as sns
from shiny import App, reactive, render, ui

tips = sns.load_dataset("tips")

# UI
app_ui = ui.page_fillable(
    ui.panel_title("Restaurant tipping"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider(
                id="slider",
                label="Bill amount",
                min=tips.total_bill.min(),
                max=tips.total_bill.max(),
                value=[tips.total_bill.min(), tips.total_bill.max()],
            ),
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
            ),
            ui.input_action_button("action_button", "Reset filter"),
        ),
        ui.layout_columns(
            ui.value_box("Total tippers", ui.output_text("total_tippers")), fill=False
        ),
    ),
)


# Server
def server(input, output, session):

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


# Create app
app = App(app_ui, server)
