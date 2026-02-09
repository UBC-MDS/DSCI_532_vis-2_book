from palmerpenguins import load_penguins
from plotnine import aes, geom_histogram, ggplot, theme_minimal

dat = load_penguins().dropna()
dat.head()

species = "Adelie"  # selected species
sel = dat.loc[dat.species == species]  # selected data

(
    ggplot(aes(x="bill_length_mm"))
    + geom_histogram(dat, fill="#C2C2C4", binwidth=1)
    + geom_histogram(sel, fill="#447099", binwidth=1)
    + theme_minimal()
)
