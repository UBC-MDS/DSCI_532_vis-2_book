from shiny.express import ui

ui.input_radio_buttons(
    id="species",
    label="Species",
    choices=["Adelie", "Gentoo", "Chinstrap"],
)
