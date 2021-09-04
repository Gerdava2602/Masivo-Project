#Dash app that use the prediction models to predict important offer info. The predicted variable is the number of people that the system may be able to transport
from dash_bootstrap_components._components import Label
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import plotly.express as px
from dash.dependencies import Input, Output, State
from datetime import date
import pandas as pd
from app.variables import variables
import numpy as np
import tensorflow as tf
from sklearn.ensemble import RandomForestRegressor
from joblib import dump, load
from dash.exceptions import PreventUpdate
import sklearn.ensemble.forest
import numpy as np


app1 = DjangoDash('oferta_model', external_stylesheets=[dbc.themes.BOOTSTRAP])

table = pd.DataFrame(columns=['Day', 'Month','Hour','Day of week','Valance','prediction'])

cenefas = pd.read_csv("core/static/cenefas_posicion_geo.csv")

controls = dbc.Card(
    # Totalization settings
    [
            dbc.FormGroup(
                [
                    dbc.Label('Hour',id='laber_one'),
                    dcc.Dropdown(
                        id='Hora',
                        options=[
                            {"label": col, "value": col} for col in range(24)
                        ],
                        multi=False
                    ),
                    
                    dbc.Label('Month'),
                    dcc.Dropdown(
                        id='Mes',
                        options=[
                            {"label": col, "value": col} for col in range(1,13)
                        ],
                        multi=False
                    ),

                    dbc.Label('Day'),
                    dcc.Dropdown(
                        id='Dia',
                        options=[
                            {"label": col, "value": col} for col in range(1,32)
                        ],
                        multi=False
                    ),
                
                    dbc.Label('Day of week'),
                    dcc.Dropdown(
                        id='Dia_semana',
                        options=[
                            {"label": col, "value": col} for col in range(0,7)
                        ],
                        multi=False
                    ),

                
                    dbc.Label('Valance'),
                    dcc.Input(
                        id="Cenefa",
                        type='Text',
                        placeholder="Cenefa",
                    ),

                    dbc.Label('Last prediction'),
                    dcc.Input(
                        id="last",
                        type='Text',
                        readOnly=True,
                    ),
                    dbc.Button("Add", id='add',color="primary", className="mr-1"),
                    dbc.Button("Reset", id='reset',color="primary", className="mr-1"),
                    
                ]
            )
        
    ],
    body=True,
)


app1.layout = dbc.Container(
    [
        html.H1("Offer forecast"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col([controls]),
                dbc.Col([
                    dbc.Table.from_dataframe(table, bordered=True,
                    hover=True,
                    responsive=True,
                    striped=True),
                    dbc.Button("download", id='dn',color="primary", className="mr-1"),
                    dcc.Download(id="download"),
                ], id='table_col')
            ],
            align="center",
        ),
    ],
    fluid=True,
)


@app1.callback(
        [Output("table_col", "children"), Output('last', 'value')],
        [Input("add", "n_clicks"), Input('reset', 'n_clicks'),State('Mes','value'), State('Dia','value'), State('Hora','value'), State('Dia_semana','value'), State('Cenefa','value')],
        prevent_initial_call=True
)
def return_table(*columns, **kwargs):
    if None in columns[2:]:
        raise PreventUpdate
    global table
    
    #Elección de Cluster
    ro = list(columns[2:-1])
    cenefa = cenefas[cenefas['CENEFA'] == columns[-1].upper()]
    if cenefa.empty:
        return [dbc.Table.from_dataframe(table),dbc.Button("download", id='dn',color="primary", className="mr-1"),
                    dcc.Download(id="download"),], 'Cenefa no encontrada'
    ro.append(float(cenefa.iloc[0]['Latitud']))
    ro.append(float(cenefa.iloc[0]['Longitud']))
    cluster = variables.oferta
    cluster = cluster[cluster['paradero_cenefa'].str.lower() == columns[-1].lower()]
    if cluster.empty:
        cluster = 0
    else:
        cluster = cluster.iloc[0]['cluster']

    ctx = kwargs['callback_context'].triggered[0]['prop_id'].split('.')[0]
    if ctx == 'add':   
        model = variables.models_oferta[int(float(cluster))]
        predict_table = table.copy()
        predict_table = predict_table.append(pd.Series(ro[:-2]+[columns[-1],model.predict(pd.Series(ro).to_frame().T)[0]], index=table.columns), ignore_index=True)
        table = predict_table   
        return [dbc.Table.from_dataframe(predict_table, bordered=True,
                        hover=True,
                        responsive=True,
                        striped=True), dbc.Button("download", id='dn',color="primary", className="mr-1"),
                    dcc.Download(id="download"),], model.predict(pd.Series(ro).to_frame().T)[0]
    elif ctx=='reset':
        reset_table =  pd.DataFrame(columns=['Day', 'Month','Hour','Day of week','Valance','prediction'])
        table = reset_table
        return [dbc.Table.from_dataframe(reset_table),dbc.Button("download", id='dn',color="primary", className="mr-1"),
                    dcc.Download(id="download"),], ''


@app1.callback([Output("download", "data")], Input(component_id="dn", component_property="n_clicks"), prevent_initial_call=True)
def generate_csv(n_clicks):
    global table
    return [dcc.send_data_frame(table.to_csv, filename= "predicciones_oferta.csv")]
