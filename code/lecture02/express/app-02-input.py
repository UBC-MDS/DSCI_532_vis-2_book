from shiny.express import ui

# title
ui.page_opts(title="Restaurant tipping", fillable=True)
# sidebar
with ui.sidebar(open="desktop"):
    ui.input_slider(
        id="slider",
        label="Bill amount",
        min=0,
        max=100,
        value=[0, 100],
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
        "Value 1"
    with ui.value_box():
        "Average tip"
        "Value 2"
    with ui.value_box():
        "Average bill"
        "Value 3"
# second row of cards
with ui.layout_columns(col_widths=[6, 6]):
    with ui.card(full_screen=True):
        ui.card_header("Tips data")
        "Tips DataFrame"
    with ui.card(full_screen=True):
        ui.card_header("Total bill vs tip")
        "Scatterplot"
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Tip percentages")
        "ridgeplot"
