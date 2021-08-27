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

app = DjangoDash('clusters')
external_stylesheets=['https://codepen.io/amyoshino/pen/jzXypZ.css']
app.css.append_css({
    "external_url": external_stylesheets
})

stations = pd.read_csv("core/static/mapa.csv")


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([


    html.H1("Uso y clusterización de mapas SITP - Masivo Capital",
            style={'text-align': 'center'}),

    html.Div([
        dcc.Dropdown(id="slct_type",
                     options=[
                         {"label": "Ver Clusters", "value": "cluster"},
                         {"label": "Ver Frecuencia", "value": "count"}],
                     multi=False,
                     value="count",
                     style={'width': "40%", 'display': 'inline-block'}
                     ),
        html.Div(id='output_container', children=[]),
    ]),
    html.Div([
        dcc.Dropdown(id="slct_cluster",
                     options=[
                         {"label": "All", "value": -1},
                         {"label": "0", "value": 0},
                         {"label": "1", "value": 1},
                         {"label": "2", "value": 2},
                         {"label": "3", "value": 3},
                         {"label": "4", "value": 4},
                     ],
                     multi=True,
                     value=-1,
                     style={'width': "40%", 'display': 'inline-block'}
                     ),

    ]),
    
    dcc.Graph(id='stations', figure={}),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='stations', component_property='figure')],
    [Input(component_id='slct_type', component_property='value')],
    [Input(component_id='slct_cluster', component_property='value')],


)
def update_graph(option_slctd, cluster_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The type chosen by user was: {}".format(option_slctd)
    container_cluster = "The cluster selectet by user was {}".format(
        cluster_slctd)

    dff = stations.copy()

    if cluster_slctd is not -1:
        dff = dff[dff["cluster"] == cluster_slctd]
    else:
        pass

    # Plotly Express
    fig = px.scatter_mapbox(dff, lat="lat", lon="lon", hover_name="cenefa", color=option_slctd, hover_data=["count", "cluster"],
                            color_discrete_sequence='["fuchsia"]', zoom=10, height=1000)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return container, fig


