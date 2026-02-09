import altair as alt
from palmerpenguins import load_penguins

dat = load_penguins().dropna()

species = "Adelie"  # selected species
sel = dat.loc[dat.species == species]  # selected data

# base histogram for all data
base = (
    alt.Chart(dat)
    .mark_bar(color="#C2C2C4", binSpacing=0)
    .encode(
        alt.X("bill_length_mm:Q", bin=alt.Bin(step=1), title="bill_length_mm"),
        alt.Y("count()", title="count"),
    )
)

# overlay histogram for selected species
overlay = (
    alt.Chart(sel)
    .mark_bar(color="#447099", binSpacing=0)
    .encode(alt.X("bill_length_mm:Q", bin=alt.Bin(step=1)), alt.Y("count()"))
)

# layer the charts
base + overlay
