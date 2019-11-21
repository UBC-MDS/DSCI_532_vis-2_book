import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import altair as alt
import vega_datasets

app = dash.Dash(__name__, assets_folder='assets')
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash app with pure Altair HTML'


def make_plot(xval = 'Displacement'):
    # Don't forget to include imports

    typeDict = {'Displacement':'quantitative',
                'Cylinders':'quantitative',
                'Miles_per_Gallon':'quantitative'
    }

    # Create a plot of the Displacement and the Horsepower of the cars dataset

    chart = alt.Chart(vega_datasets.data.cars.url).mark_point(size=90).encode(
                alt.X(xval,type=typeDict[xval]),
                alt.Y('Horsepower:Q', title = 'Horsepower (h.p.)'),
                tooltip = ['Horsepower:Q', 'Displacement:Q']
            ).properties(title='Horsepower vs. Displacement',
                        width=500, height=350).interactive()

    return chart

app.layout = html.Div([

    html.Div(
        className="app-header",
        children=[
            html.Div('Plotly Dash', className="app-header--title")
        ]
    ),    

    ### Add Tabs to the top of the page
    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Lecture 1', value='tab-1'),
        dcc.Tab(label='Lecture 2', value='tab-2'),
        dcc.Tab(label='Lecture 3', value='tab-3'), 
        dcc.Tab(label='Lecture 4', value='tab-4'), 
    ]),    

    ### ADD CONTENT HERE like: html.H1('text'),
    html.H1('This is my first dashboard'),
    html.H2('This is a subtitle'),

    html.H3('Here is an image'),
    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
            width='10%'),

    html.H3('Here is our first plot:'),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='450',
        width='1800',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_plot().to_html()
        ################ The magic happens here
        ),

    dcc.Markdown('''
    ### Dash and Markdown
                '''),

    ## these two components are related to dropdown
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC',
        style=dict(width='45%',
              verticalAlign="middle"
              )
        ),
        html.Div(id='dd-output'),

        dcc.Dropdown(
        id='dd-chart',
        options=[
            {'label': 'Miles_per_Gallon', 'value': 'Miles_per_Gallon'},
            {'label': 'Cylinders', 'value': 'Cylinders'},
            {'label': 'Displacement', 'value': 'Displacement'}
        ],
        value='Displacement',
        style=dict(width='45%',
              verticalAlign="middle"
              )
        ),
])

@app.callback(
    dash.dependencies.Output('dd-output', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return 'You have selected {}'.format(value)

@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('dd-chart', 'value')])
def update_plot(xaxis_column_name):

    updated_plot = make_plot(xaxis_column_name).to_html()

    return updated_plot

if __name__ == '__main__':
    app.run_server(debug=True)
