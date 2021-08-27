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

app1 = DjangoDash('prueba', external_stylesheets=[dbc.themes.BOOTSTRAP])

#table = get_table('historico_demanda_v2')
table = variables.historico_demanda
table['id_vehiculo'] = table['id_vehiculo'].astype('category')

drops = ['nombre_de_ruta', 'id_vehiculo']

filtered_tables = {
    '0' : table.groupby(['descripcion', 'nombre_de_ruta','id_vehiculo'])['demanda'].sum().to_frame().reset_index(),
    '1' : table.groupby(['dia', 'nombre_de_ruta','id_vehiculo'])['demanda'].sum().to_frame().reset_index(),
    '2' : table.groupby(['semana', 'nombre_de_ruta','id_vehiculo'])['demanda'].sum().to_frame().reset_index()
}

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
                    {"label": "Dias", "value": 1},
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
    global fig
    start_date = columns[-3]
    end_date = columns[-2]
    #if start_date is not None and end_date is not None:
        #start_date_object = date.fromisoformat(start_date)
        #end_date_object = date.fromisoformat(end_date)

    data = filtered_tables[str(columns[-1])][(filtered_tables[str(columns[-1])][drops[0]].isin(columns[0])) &
                            (filtered_tables[str(columns[-1])][drops[1]].isin(columns[1]))] #&
                            #(start_date <= filtered_tables[str(columns[-1])]['Fecha_clearing'] <= end_date)]

    if columns[-1] == 0:
        fig = px.bar(data, x='descripcion', y='demanda', color='id_vehiculo', facet_row="nombre_de_ruta", )
    elif columns[-1] == 1:
        fig = px.bar(data, x='dia', y='demanda', color='id_vehiculo', facet_row="nombre_de_ruta", )
    elif columns[-1] == 2:
        fig = px.bar(data, x='semana', y='demanda', color='id_vehiculo', facet_row="nombre_de_ruta", )
    return fig


if __name__ == "__main__":
    app1.run_server(host="0.0.0.0", port="8050", debug=True)