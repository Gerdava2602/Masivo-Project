import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import plotly.express as px
from dash.dependencies import Input, Output
from datetime import date
import pandas as pd
from app.variables import variables

def get_inputs():
    inputs = []
    for col in drops:
        inputs.append(Input(str(col), 'value'))
    return inputs +[Input('date-range', 'start-date'), Input('date-range', 'end-date'),Input('totalization','value')]

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

app1 = DjangoDash('oferta', external_stylesheets=[dbc.themes.BOOTSTRAP])


table = variables.oferta
table['numero_bus'] = table['numero_bus'].astype('category')
table['linea'] = table['linea'].astype('category')

drops = ['linea', 'numero_bus','nodo']

filtered_tables = {
    #'0' : table.groupby(['descripcion', 'nombre_de_ruta','id_vehiculo'])['demanda'].count().to_frame().reset_index(),
    '1' : table.groupby(['día', 'linea', 'numero_bus','nodo'])['fecha'].count().to_frame().reset_index(),
    #'2' : table.groupby(['semana', 'nombre_de_ruta','id_vehiculo'])['demanda'].count().to_frame().reset_index(),
    '3' : table.groupby(['mes', 'linea','numero_bus','nodo'])['fecha'].count().to_frame().reset_index(),
}

filtered_tables['1']['fecha'] = filtered_tables['1']['fecha']*80
filtered_tables['3']['fecha'] = filtered_tables['3']['fecha']*80


fig = None

controls = dbc.Card(
    # Totalization settings
    [
        dbc.FormGroup(
            [
            dbc.Label("Choose the totalization"),
            dbc.RadioItems(
                options=[
                    {"label": "Franjas", "value": 0},
                    {"label": "Días", "value": 1},
                    {"label": "Semanas", "value": 2},
                    {"label": "Meses", "value": 3},
                ],
                value=0,
                id="totalization",
                inline=True,
            ),
        ])
    ]
    #Filters
    +get_forms(table)+
    #Date Range
    [
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=date(2021, 1, 1),
            max_date_allowed=date(2021, 5, 31),
            initial_visible_month=date(2021, 4, 5),
            end_date=date(2021, 5, 31)
        ),
    ],
    
    body=True,
)


app1.layout = dbc.Container(
    [
        html.H1("Oferta"),
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
    global fig
    start_date = columns[-3]
    end_date = columns[-2]
    #if start_date is not None and end_date is not None:
        #start_date_object = date.fromisoformat(start_date)
        #end_date_object = date.fromisoformat(end_date)

    data = filtered_tables[str(columns[-1])][(filtered_tables[str(columns[-1])][drops[0]].isin(columns[0])) &
                            (filtered_tables[str(columns[-1])][drops[1]].isin(columns[1])) &
                            (filtered_tables[str(columns[-1])][drops[2]].isin(columns[2]))] #&
                            #(start_date <= filtered_tables[str(columns[-1])]['Fecha_clearing'] <= end_date)]
    if len(columns[0]) < 4: 
        if columns[-1] == 0:
            fig = px.bar(data, x='descripcion', y='demanda', color='id_vehiculo', facet_row="nombre_de_ruta", )
        elif columns[-1] == 1:
            fig = px.bar(data, x='día', y='fecha', color='numero_bus', facet_row="linea", )
        elif columns[-1] == 2:
            fig = px.bar(data, x='semana', y='demanda', color='id_vehiculo', facet_row="nombre_de_ruta", )
        elif columns[-1] == 3:
            fig = px.bar(data, x='mes', y='fecha', color='numero_bus', facet_row="linea", )
    else:
        if columns[-1] == 0:
            fig = px.bar(data, x='descripcion', y='demanda', color='id_vehiculo',  )
        elif columns[-1] == 1:
            fig = px.bar(data, x='día', y='demanda', color='id_vehiculo',  )
        elif columns[-1] == 2:
            fig = px.bar(data, x='semana', y='demanda', color='id_vehiculo', )
        elif columns[-1] == 3:
            fig = px.bar(data, x='mes', y='fecha', color='numero_bus')
    return fig