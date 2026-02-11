from shiny import reactive
from shiny.express import input, render, ui

ui.input_slider("x", "Slider value", min=0, max=100, value=10)


# we need to make a calculation from an input value
@render.text
def x_squared_text():
    return f"Squared value: {input.x() ** 2}"


# we can save this calculation to be used later
@reactive.calc
def x_squared():
    return input.x() ** 2


# we can use that saved calculation
@render.text
def x_squared_calc_text():
    return f"Saved squared: {x_squared()}"


# we can build on top of that saved calculation
@render.text
def x_squared_half_calc_text():
    return f"Build on squared value: {x_squared() / 2}"


# we don't need to re-calculate everything from the input again
@render.text
def x_squared_half_text():
    return f"Recalculate from input: {input.x() ** 2 / 2}"
