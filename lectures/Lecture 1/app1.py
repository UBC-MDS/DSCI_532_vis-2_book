import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Dash app with pure Altair HTML'

app.layout = html.Div([

    ### ADD CONTENT HERE like: html.H1('text'),

    ### Let's now add an iframe to bring in HTML content

    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='1500',
        width='2000',
        style={'border-width': '5px'},
        srcDoc=open('complex_chart.html').read()
        ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
