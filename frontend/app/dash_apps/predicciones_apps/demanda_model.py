#Dash app that use the prediction models to predict important demand info. The predicted variables may be the number of people that need transport
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
from tensorflow import keras
from dash.exceptions import PreventUpdate


app1 = DjangoDash('demanda_model', external_stylesheets=[dbc.themes.BOOTSTRAP])

clusters = {
    0: variables.cluster_0,
    1: variables.cluster_1,
    2: variables.cluster_2,
    3: variables.cluster_3,
    4: variables.cluster_4,
}

table = pd.DataFrame(columns=['Month','Day', 'Hour','Day of week','type of travel','line','route','Valance','prediction'])

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
                            {"label": col, "value": col} for col in ['Friday','Monday','Saturday','Sunday','Thursday','Tuesday','Wednesday',]
                        ],
                        multi=False
                    ),
                
                    dbc.Label('Type of travel'),
                    dcc.Dropdown(
                        id='viaje',
                        options=[
                            {"label": col, "value": col} for col in ['Transbordo', 'Viaje Inicial']
                        ],
                        multi=False
                    ),

                
                    dbc.Label('Line'),
                    dcc.Input(
                        id="Linea",
                        type='number',
                        placeholder="Linea SAE",
                    ),

                    dbc.Label('Route'),
                    dcc.Input(
                        id="Ruta",
                        type='number',
                        placeholder="Ruta",
                    ),
                    dbc.Label('Valance'),
                    dcc.Input(
                        id="Cenefa",
                        type='Text',
                        placeholder="Cenefa",
                    ),
                    dbc.Label('latest prediction'),
                    dcc.Input(
                        id = 'last',
                        type='text',
                        readOnly=True
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
        html.H1("Demand forecast"),
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
        [Input("add", "n_clicks"), Input('reset', 'n_clicks'),State('Mes','value'), State('Dia','value'), State('Hora','value'), State('Dia_semana','value'), State('viaje','value'), State('Linea','value'), State('Ruta','value'), State('Cenefa','value')],
        prevent_initial_call=True
)
def return_table(*columns, **kwargs):
    if None in columns[2:]:
        raise PreventUpdate
    global table
    cluster = variables.validaciones
    cluster = cluster[(cluster['parada'].astype('str').str.upper() == columns[-1].upper())]
    if cluster.empty:
        return [dbc.Table.from_dataframe(table),dbc.Button("download", id='dn',color="primary", className="mr-1"),
                    dcc.Download(id="download"),], 'Cenefa no encontrada'
    else:
        cluster = int(float(cluster.iloc[0]['cluster']))
    ro = []
    converted_columns = []
    ctx = kwargs['callback_context'].triggered[0]['prop_id'].split('.')[0]
    if ctx == 'add':   
        #Convert the info for the model processing
        for i in columns:
            try:
                converted_columns.append(str(float(i)))
            except:
                converted_columns.append(i)

        for i in range(len(clusters[cluster].columns)):
                if i < 3:   
                    ro.append(converted_columns[i+2])
                else:
                    if clusters[cluster].columns[i] in converted_columns[5:]:
                        ro.append(1)
                    else:
                        ro.append(0)

        ro = clusters[cluster].append(pd.Series(ro, index=clusters[cluster].columns), ignore_index=True).astype('float')
        model = variables.models[cluster]
        converted_columns.append([model.predict(ro)[0][0]])
        predict_table = table.copy()
        predict_table = predict_table.append(pd.Series(converted_columns[2:], index=table.columns), ignore_index=True)
        table = predict_table   
        return [dbc.Table.from_dataframe(predict_table, bordered=True,
                        hover=True,
                        responsive=True,
                        striped=True), dbc.Button("download", id='dn',color="primary", className="mr-1"),
                    dcc.Download(id="download"),], model.predict(ro)
    elif ctx=='reset':
        reset_table =  pd.DataFrame(columns=['Month','Day', 'Hour','Day of week','type of travel','line','route','Valance','prediction'])
        table = reset_table
        return [dbc.Table.from_dataframe(reset_table),dbc.Button("download", id='dn',color="primary", className="mr-1"),
                    dcc.Download(id="download"),], ''


@app1.callback([Output("download", "data")], Input(component_id="dn", component_property="n_clicks"), prevent_initial_call=True)
def generate_csv(n_clicks):
    global table
    return [dcc.send_data_frame(table.to_csv, filename= "predicciones_demanda.csv")]
