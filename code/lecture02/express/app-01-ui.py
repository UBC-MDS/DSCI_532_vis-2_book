from shiny.express import ui

# title
ui.page_opts(title="Restaurant tipping", fillable=True)
# sidebar (empty for now)
with ui.sidebar(open="desktop"):
    "sidebar inputs"
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
    with ui.card(full_screen=True):
        ui.card_header("Total bill vs tip")
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Tip percentages")
