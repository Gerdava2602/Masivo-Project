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


app1 = DjangoDash('demanda_model', external_stylesheets=[dbc.themes.BOOTSTRAP])

clusters = {
    0: variables.cluster_0,
    1: variables.cluster_1,
    2: variables.cluster_2,
    3: variables.cluster_3,
    4: variables.cluster_4,
}

table = pd.DataFrame(columns=['Mes','Dia', 'Hora','Dia de la semana','tipo_viaje','linea','ruta','predicción'])

controls = dbc.Card(
    # Totalization settings
    [
            dbc.FormGroup(
                [
                    dbc.Label('Hora',id='laber_one'),
                    dcc.Dropdown(
                        id='Hora',
                        options=[
                            {"label": col, "value": col} for col in range(24)
                        ],
                        multi=False
                    ),
                    
                    dbc.Label('Mes'),
                    dcc.Dropdown(
                        id='Mes',
                        options=[
                            {"label": col, "value": col} for col in range(1,13)
                        ],
                        multi=False
                    ),

                    dbc.Label('Dia'),
                    dcc.Dropdown(
                        id='Dia',
                        options=[
                            {"label": col, "value": col} for col in range(1,32)
                        ],
                        multi=False
                    ),
                
                    dbc.Label('Dia de la semana'),
                    dcc.Dropdown(
                        id='Dia_semana',
                        options=[
                            {"label": col, "value": col} for col in ['Friday','Monday','Saturday','Sunday','Thursday','Tuesday','Wednesday',]
                        ],
                        multi=False
                    ),
                
                    dbc.Label('Tipo del viaje'),
                    dcc.Dropdown(
                        id='viaje',
                        options=[
                            {"label": col, "value": col} for col in ['Transbordo', 'Viaje Inicial']
                        ],
                        multi=False
                    ),

                
                    dbc.Label('Linea'),
                    dcc.Input(
                        id="Linea",
                        type='number',
                        placeholder="Linea SAE",
                    ),

                    dbc.Label('Ruta'),
                    dcc.Input(
                        id="Ruta",
                        type='number',
                        placeholder="Ruta",
                    ),
                    dbc.Label('latest prediction'),
                    dcc.Input(
                        id = 'last',
                        type='text'
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
        html.H1("Demanda model"),
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
                ], id='table_col')
            ],
            align="center",
        ),
    ],
    fluid=True,
)

'''
@app1.callback(
        [Output("table_col", "children")],
        [Input("reset", "n_clicks")]
)
def reset(*clicks):
    global table
    reset_table =  pd.DataFrame(columns=['Mes','Dia', 'Hora','Dia de la semana','tipo_viaje','linea','ruta','predicción'])
    table = reset_table
    return dbc.Table.from_dataframe(reset_table)
'''

@app1.callback(
        [Output("table_col", "children"), Output('last', 'value')],
        [Input("add", "n_clicks") ,State('Mes','value'), State('Dia','value'), State('Hora','value'), State('Dia_semana','value'), State('viaje','value'), State('Linea','value'), State('Ruta','value')],
        prevent_initial_call=True
)
def return_table(*columns):
    global table
    cluster = 0
    ro = []
    converted_columns = []
    #Convert the info for the model processing
    for i in columns:
        try:
            converted_columns.append(str(float(i)))
        except:
            converted_columns.append(i)

    for i in range(len(clusters[cluster].columns)):
            if i < 3:   
                ro.append(converted_columns[i+1])
            else:
                if clusters[cluster].columns[i] in converted_columns:
                    ro.append(1)
                else:
                    ro.append(0)

    ro = clusters[cluster].append(pd.Series(ro, index=clusters[cluster].columns), ignore_index=True).astype('float')
    model = variables.models[cluster]
    converted_columns.append([model.predict(ro)[0][0]])
    predict_table = table.copy()
    predict_table = predict_table.append(pd.Series(converted_columns[1:], index=table.columns), ignore_index=True)
    table = predict_table   
    return [dbc.Table.from_dataframe(predict_table, bordered=True,
                    hover=True,
                    responsive=True,
                    striped=True), dbc.Button("Download", id='dn',color="primary", className="mr-1")], model.predict(ro)


@app1.callback([Output("download", "data")], Input(component_id="dn", component_property="n_clicks"), prevent_initial_call=True)
def generate_csv(n_clicks):
    global table
    return [dcc.send_data_frame(table.to_csv, filename= "predicciones_demanda.csv")]



