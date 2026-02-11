import pandas as pd
import seaborn as sns
from shiny import App, render, ui, reactive

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
            open="desktop",
        ),
        ui.layout_columns(
            ui.value_box("Total tippers", ui.output_text("total_tippers")),
            ui.value_box("Average tip", ui.output_text("average_tip")),
            ui.value_box("Average bill", ui.output_text("average_bill")),
            fill=False,
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
        return str(tips_filtered.shape[0])

    @render.text
    def average_tip():
        idx1 = tips.total_bill.between(
            left=input.slider()[0],
            right=input.slider()[1],
            inclusive="both",
        )
        idx2 = tips.time.isin(input.checkbox_group())
        tips_filtered = tips[idx1 & idx2]
        perc = tips_filtered.tip / tips_filtered.total_bill
        return f"{perc.mean():.1%}"

    @render.text
    def average_bill():
        idx1 = tips.total_bill.between(
            left=input.slider()[0],
            right=input.slider()[1],
            inclusive="both",
        )
        idx2 = tips.time.isin(input.checkbox_group())
        tips_filtered = tips[idx1 & idx2]
        bill = tips_filtered.total_bill.mean()
        return f"${bill:.2f}"


# Create app
app = App(app_ui, server)
