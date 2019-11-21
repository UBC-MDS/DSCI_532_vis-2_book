import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import altair as alt
import vega_datasets

app = dash.Dash(__name__, assets_folder='assets',#external_stylesheets=external_stylesheets
)
server = app.server
app.title = 'Dash app with pure Altair HTML'

def make_plot():

    # Don't forget to include imports

    # Create a plot of the Displacement and the Horsepower of the cars dataset

    chart = alt.Chart(vega_datasets.data.cars.url).mark_point(size=90).encode(
                alt.X('Displacement:Q', title = 'Displacement (mm)'),
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
        srcDoc=open('chart.html').read()
        ################ The magic happens here
        ),
    html.P('We created the chart above using the <b>Altair</b> library in a jupyter notebook.'),
    
    dcc.Markdown('''
    ### Dash and Markdown
    Rather than writing and styling your text using pure html, 
    dash  actually supports Markdown syntax as well.

    In fact, I would recommend you use Markdown as it's more **readable** and *easier* to use with git.
    
    Unordered List syntax works out of the box:
    - List 1
    - List 2
    - List 3

    as well as an ordered list:
    1. One
    1. Two
    1. Three

    ### Do images work well in a Dash Markdown component?

    Yes, but just like in regular markdown, you cannot control img sizes, need HTML for that.
    Probably better to use the Dash Img() component (see above).
    You can add the image as-is by turning removing the triple ticks from the code line below:

    ```![Image](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png)```

    ## More Dash Core Components

    So far we have used just a few of the Dash components: 
    `html.H1`, `html.Img`, `html.P`, and `dcc.Markdown`.
    There are many other, much more useful components.
    A full list of the core components is [here](https://dash.plot.ly/dash-core-components) and the exhaustive list of html components can be found [here](https://dash.plot.ly/dash-html-components).

    Let's start by adding a few of these components.
    Note that the components won't really do very much at the moment, but we will soon learn how to use these components to control our plots.

    ![](https://media1.tenor.com/images/99a1288a3057dc8e9ff7ebf5d46baee3/tenor.gif?itemid=15254127)
    ![](https://media1.tenor.com/images/f708e56b6ab99de21228c95203c7af8e/tenor.gif?itemid=13942585)
    
    Gif sources: [1](https://tenor.com/view/yoda-patience-you-must-have-patience-gif-15254127) and [2](https://tenor.com/view/teach-you-yoda-star-wars-mentor-teach-you-iwill-gif-13942585)
    
    ### Dropdowns

    To add a dropdown,  in the app.layout, and inside the list of components in `html.Div`, you can add this code:

    ```
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    )  
    ```
    ### Slider

    Slider bars are easy too:
    ```
    dcc.Slider(
        min=0,
        max=9,
        marks={i: 'Label {}'.format(i) for i in range(10)},
        value=5,
    )  
    ```
    ### Tabs - an essential dash core component (dcc)!

    You can add tabs to your dashboard in a similar way:
    ```
    ### Add Tabs to the top of the page
    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Lecture 1', value='tab-1'),
        dcc.Tab(label='Lecture 2', value='tab-2'),
        dcc.Tab(label='Lecture 3', value='tab-3'), 
        dcc.Tab(label='Lecture 4', value='tab-4'), 
    ]),  
    ```
    Note that you haven't quite learned how to have different content in each of the tabs, we'll learn that a little later.
    It requires setting up a Dash `callback`.
    If you're curious, you can see how it works [here](https://dash.plot.ly/dash-core-components). 
    '''),
    html.Iframe(
        height='250',
        width='10',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=open('chart.html').read()
        ################ The magic happens here
        ),

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
    html.Div(id='dd-output')
])

@app.callback(
    dash.dependencies.Output('dd-output', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return 'You have selected {}'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
