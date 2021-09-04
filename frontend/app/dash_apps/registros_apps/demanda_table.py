#Dash app that displays the table 'validaciones' from the database and let the user download it.
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from django_plotly_dash import DjangoDash
import pandas as pd
from dash.dependencies import Output, Input, State
from datetime import date
from app.variables import variables
import psycopg2
from app.variables import variables
#external_stylesheets = 'https://codepen.io/chriddyp/pen/bWLwgP.css'

table_name = 'demanda_cluster'
app = DjangoDash('validaciones_v2', external_stylesheets=[dbc.themes.BOOTSTRAP])

table = variables.validaciones.head(20)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H5(children='Select the number of registers:'),
            dcc.Input(
                    id="rows",
                    type= 'number',
                    placeholder="10",
                    min=0,
                    value=10
                ),
        ])
    ], style={'height': '10%'}),
    dbc.Row([
        dbc.Col([
            dbc.Table.from_dataframe(table, bordered=True,
            hover=True,
            responsive=True,
            striped=True),
        ]),
    ], style={'height': '100vh',
  'overflow': 'auto',
   'margin':'20px'}),
    dbc.Row([
        dbc.Col([
            html.Button("Download csv", id="btn"),  
            dcc.Download(id="download"),
        ])
    ], style={'height': '5%'})
], fluid=True)

@app.callback([Output("download", "data")], Input(component_id="btn", component_property="n_clicks"), State(component_id='rows', component_property='value'), prevent_initial_call=True)
def generate_csv(n_clicks, rows):

    new_table = variables.validaciones.head(rows)
    return [dcc.send_data_frame(new_table.to_csv, filename= table_name+".csv")]
