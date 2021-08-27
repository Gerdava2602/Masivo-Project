import dash
import dash_core_components as dcc
import dash_html_components as html

from django_plotly_dash import DjangoDash

# Read plotly example dataframe to plot barchart
import plotly.express as px
df = px.data.gapminder().query("country=='India'")

external_stylesheets=['https://codepen.io/amyoshino/pen/jzXypZ.css']

# Important: Define Id for Plotly Dash integration in Django
app = DjangoDash('dash_integration_id')

app.css.append_css({
"external_url": external_stylesheets
})
app.layout = html.Div(
    html.Div([
        # Adding one extar Div
        html.Div([
            html.H3(children='Masivo Capital'),
        ], className = 'row'),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='bar-chart',
                    figure={
                        'data': [
                            {'x': df['year'], 'y': df['pop'], 'type': 'bar', 'name': 'SF'},
                        ],
                        'layout': {
                            'title': 'Validaciones ruta 201A36'
                        }
                    }
                ),
            ], className = 'six columns'),

            html.Div([
                html.H3(children='Line chart'),
            ], className = 'row'),

            html.Div([
                dcc.Graph(
                    id='line-chart',
                    figure={
                        'data': [
                            {'x': df['year'], 'y': df['pop'], 'type': 'line', 'name': 'SF'},
                        ],
                        'layout': {
                            'title': 'Line Chart Visualization'
                        }
                    }
                )
            ], className = 'six columns')

        ], className = 'row')
    ])
)

if __name__ == '__main__':
    app.run_server(8052, debug=False)