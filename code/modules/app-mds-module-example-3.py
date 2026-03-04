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
    return ui.card(
            ui.input_selectize(
                id="species",
                label="Select Species",
                choices=species_list,
                multiple=False,
            ),
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
            fill=False
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


app_ui = ui.page_fluid(
    ui.input_action_button("add", "Add comparison"),
    ui.input_action_button("remove", "Remove"),
    ui.output_ui("comparisons")
)


def server(input, output, session):
    # Reactive value to store the list of comparison IDs
    comparison_ids = reactive.value(["comparison1"])

    # Dictionary to store server functions for cleanup
    server_functions = {}

    @reactive.effect
    @reactive.event(input.add)
    def add_comparison():
        current_ids = comparison_ids.get()
        # Generate new unique ID
        new_id = f"comparison{len(current_ids) + 1}"
        # Add new ID to the list
        comparison_ids.set(current_ids + [new_id])

    @reactive.effect
    @reactive.event(input.remove)
    def remove_comparison():
        current_ids = comparison_ids.get()
        if len(current_ids) > 1:  # Keep at least one comparison
            # Remove the last comparison
            comparison_ids.set(current_ids[:-1])

    @render.ui
    def comparisons():
        # Generate UI for all current comparisons
        current_ids = comparison_ids.get()
        comparison_uis = []

        for comp_id in current_ids:
            comparison_uis.append(comparison_ui(comp_id))

            # Initialize server for this comparison if not already done
            if comp_id not in server_functions:
                server_functions[comp_id] = comparison_server(comp_id, penguins)

        # Clean up server functions for removed comparisons
        for comp_id in list(server_functions.keys()):
            if comp_id not in current_ids:
                del server_functions[comp_id]

        return ui.layout_columns(
          *comparison_uis,
          col_widths=3
        )

    # Initialize the first comparison server
    server_functions["comparison1"] = comparison_server("comparison1", penguins)

app = App(app_ui, server)
