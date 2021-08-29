import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from django_plotly_dash import DjangoDash
import pandas as pd
from dash.dependencies import Output, Input, State
from datetime import date
from app.variables import variables
import psycopg2

#external_stylesheets = 'https://codepen.io/chriddyp/pen/bWLwgP.css'

table_name = 'validaciones_v2'
app = DjangoDash(table_name, external_stylesheets=[dbc.themes.BOOTSTRAP])


def get_table(table_name, limit=20):
    conexion = psycopg2.connect(host="team-82.cc7kkbiuuvan.us-east-2.rds.amazonaws.com", database="masivo_capital", user="team_82", password="Ds4ateam_82")
    # Creamos el cursor con el objeto conexion
    cur = conexion.cursor()
    cur.execute('SELECT * FROM '+table_name+' LIMIT '+str(limit))
    data = cur.fetchall()
    cur.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='{}'".format(table_name))
    table = pd.DataFrame(data, columns=[c[0] for c in cur])
    return table

#table = get_table(table_name)
table = get_table(table_name)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H5(children='Select the number:'),
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

    new_table = get_table(table_name, rows)
    return [dcc.send_data_frame(new_table.to_csv, filename= table_name+".csv")]
