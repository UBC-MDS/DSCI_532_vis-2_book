from shiny.express import ui

from palmerpenguins import load_penguins
from plotnine import aes, geom_histogram, ggplot, theme_minimal

ui.input_radio_buttons(
    id="species",
    label="Species",
    choices=["Adelie", "Gentoo", "Chinstrap"],
    inline=True,
)

dat = load_penguins()
species = "Adelie"
sel = dat.loc[dat.species == species]

# this will cause a TypeError: Invalid tag item type
(
    ggplot(aes(x="bill_length_mm"))
    + geom_histogram(dat, fill="#C2C2C4", binwidth=1)
    + geom_histogram(sel, fill="#447099", binwidth=1)
    + theme_minimal()
)
