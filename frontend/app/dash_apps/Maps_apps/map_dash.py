#Dash app that displays the clustering of the information and their counting
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

app = DjangoDash('clusters', external_stylesheets=[dbc.themes.BOOTSTRAP])

stations = pd.read_csv("core/static/mapa.csv")

# App layout
app.layout = dbc.Container([

    html.Div([
        html.H1("Use and clustering of the SITP maps - Masivo Capital",
                style={'text-align': 'center'}),
        
        html.Div([
            dbc.Label('Type of visualization '),
            dcc.Dropdown(id="slct_type",
                        options=[
                            {"label": "Ver Clusters", "value": "cluster"},
                            {"label": "Ver Frecuencia", "value": "count"}],
                        multi=False,
                        value="count",
                        ),
        ]),
        html.Div([
            dbc.Label('Choose the cluster '),
            dcc.Dropdown(id="slct_cluster",
                        options=[
                            {"label": "All", "value": -1},
                            {"label": "0", "value": 0},
                            {"label": "1", "value": 1},
                            {"label": "2", "value": 2},
                            {"label": "3", "value": 3},
                            {"label": "4", "value": 4},
                        ],
                        multi=False,
                        value=-1,
                        ),

        ]),
        html.Hr()
    ]),
    html.Div([
        dcc.Graph(id='stations', figure={}),
    ])
],
fluid=True,
)


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='stations', component_property='figure'),
    [Input(component_id='slct_type', component_property='value')],
    [Input(component_id='slct_cluster', component_property='value')],


)
def update_graph(option_slctd, cluster_slctd):

    dff = stations.copy()

    if cluster_slctd is not -1:
        dff = dff[dff["cluster"] == cluster_slctd]

    # Plotly Express
    fig = px.scatter_mapbox(dff, lat="lat", lon="lon", hover_name="cenefa", color=option_slctd, hover_data=["count", "cluster"],
                            color_discrete_sequence='["fuchsia"]', zoom=10, height=1000)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


