from shiny import App, ui

app_ui = ui.page_fluid(
    ui.input_radio_buttons(
        id="species",
        label="Species",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        inline=True,
    )
)


def server(input, output, session):
    pass


app = App(app_ui, server)
