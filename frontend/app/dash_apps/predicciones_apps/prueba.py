import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output
import psycopg2
import pandas as pd

def get_table(table_name):
    conexion = psycopg2.connect(host="team-82.cc7kkbiuuvan.us-east-2.rds.amazonaws.com", database="masivo_capital", user="team_82", password="Ds4ateam_82")
    # Creamos el cursor con el objeto conexion
    cur = conexion.cursor()
    cur.execute('SELECT * FROM '+table_name+' LIMIT 500')
    data = cur.fetchall()
    cur.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='{}'".format(table_name))
    table = pd.DataFrame(data, columns=[c[0] for c in cur])
    table['id_vehiculo'] = table['id_vehiculo'].astype('category')
    return table

def get_inputs():
    inputs = []
    for col in drops:
        inputs.append(Input(str(col), 'value'))
    return inputs

def get_forms(table):
    forms = []
    for column in drops:
        forms.append(dbc.FormGroup(
            [
                dbc.Label(column),
                dcc.Dropdown(
                    id=str(column),
                    options=[
                        {"label": col, "value": col} for col in list(table[column].unique())
                    ],
                    multi=True
                ),
            ]
        ))
    return forms

app1 = DjangoDash('prueba')

table = get_table('historico_demanda_v2')

drops = ['nombre_de_ruta', 'id_vehiculo']

controls = dbc.Card(
    get_forms(table),
    body=True,
)


app1.layout = dbc.Container(
    [
        html.H1("Demanda"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="graph"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)    

inputs = get_inputs()

@app1.callback(
        Output("graph", "figure"),
        inputs,
)
def make_graph(*columns):
    data = table[(table[drops[0]].isin(columns[0])) & (table[drops[1]].isin(columns[1]))]
    demanda = data.groupby(['descripcion', 'nombre_de_ruta','id_vehiculo'])['demanda'].sum()
    demanda = demanda.to_frame().reset_index()

    return px.bar(demanda, x='descripcion', y='demanda', color='id_vehiculo', facet_row="nombre_de_ruta", )


if __name__ == "__main__":
    app1.run_server(host="0.0.0.0", port="8050", debug=True)