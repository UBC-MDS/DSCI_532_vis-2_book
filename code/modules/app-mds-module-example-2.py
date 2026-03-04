# moves everything into a module

from palmerpenguins import load_penguins
import plotly.express as px
from shiny import App, module, render, ui, reactive
from shinywidgets import render_plotly, output_widget

plotly_modebar_remove = ["zoom", "pan", "lasso", "select", "autoscale"]

penguins = load_penguins()
penguins = penguins.dropna()
species_list = sorted(penguins['species'].unique())

@module.ui
def comparison_ui():
  return ui.layout_columns(
        ui.card(
            ui.input_selectize(
                id="species",
                label="Select Species",
                choices=species_list,
                multiple=False,
            ),
            ui.input_action_button("add", "+", width="25px"),
            ui.input_action_button("remove", "-", width="25px"),
            ui.value_box(
                title="Average Bill Length (mm)",
                value=ui.output_ui("avg_bill_length_mm")
            ),
            ui.value_box(
                title="Average Bill Depth (mm)",
                value=ui.output_ui("avg_bill_depth_mm")
            ),
            ui.value_box(
                title="Average Flipper Length (mm)",
                value=ui.output_ui("avg_flipper_length_mm")
            ),
            ui.card(
                output_widget("plot_year"),
            ),
            ui.card(
                output_widget("plot_sex"),
            ),
        ),
        col_widths=(4),
    )

@module.server
def comparison_server(input, output, session, data):
    @reactive.calc
    def penguin_species():
        return penguins.loc[penguins['species'] == input.species()]

    @render.text
    def avg_bill_length_mm():
        return f"{penguin_species()['bill_length_mm'].mean() :.2f}"

    @render.text
    def avg_bill_depth_mm():
        return f"{penguin_species()['bill_depth_mm'].mean() :.2f}"


    @render.text
    def avg_flipper_length_mm():
        return f"{penguin_species()['flipper_length_mm'].mean() :.2f}"


    @render_plotly
    def plot_year():
        counts = penguin_species()["year"].value_counts().reset_index()
        fig = px.bar(counts, x="year", y="count")
        fig.update_layout(
            modebar_remove=plotly_modebar_remove,
        )
        return fig

    @render_plotly
    def plot_sex():
        counts = penguin_species()["sex"].value_counts().reset_index()
        fig = px.pie(counts, values="count", names="sex")
        fig.update_layout(
            modebar_remove=plotly_modebar_remove,
        )
        return fig


app_ui = ui.page_auto(
  comparison_ui("comparison1")
)


def server(input, output, session):
  comparison_server("comparison1", penguins)

app = App(app_ui, server)
