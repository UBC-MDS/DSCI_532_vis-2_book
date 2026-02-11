from shiny import App, ui

# UI
app_ui = ui.page_fillable(
    ui.panel_title("Restaurant tipping"),
    ui.layout_sidebar(
        ui.sidebar("sidebar inputs", open="desktop"),
        ui.layout_columns(
            ui.value_box("Total tippers", "Value 1"),
            ui.value_box("Average tip", "Value 2"),
            ui.value_box("Average bill", "Value 3"),
            fill=False,
        ),
        ui.layout_columns(
            ui.card(ui.card_header("Tips data"), full_screen=True),
            ui.card(ui.card_header("Total bill vs tip"), full_screen=True),
            col_widths=[6, 6],
        ),
        ui.layout_columns(ui.card(ui.card_header("Tip percentages"), full_screen=True)),
    ),
)


# Server
def server(input, output, session):
    pass


# Create app
app = App(app_ui, server)
