from shiny import App, ui

# UI
app_ui = ui.page_fillable(
    ui.panel_title("Restaurant tipping"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider(
                id="slider",
                label="Bill amount",
                min=0,
                max=100,
                value=[0, 100],
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
            ui.value_box("Total tippers", "Value 1"),
            ui.value_box("Average tip", "Value 2"),
            ui.value_box("Average bill", "Value 3"),
            fill=False,
        ),
        ui.layout_columns(
            ui.card(ui.card_header("Tips data"), "Tips DataFrame", full_screen=True),
            ui.card(
                ui.card_header("Total bill vs tip"), "Scatterplot", full_screen=True
            ),
            col_widths=[6, 6],
        ),
        ui.layout_columns(
            ui.card(ui.card_header("Tip percentages"), "ridgeplot", full_screen=True)
        ),
    ),
)


# Server
def server(input, output, session):
    pass


# Create app
app = App(app_ui, server)
