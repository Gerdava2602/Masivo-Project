#Dash app that creates visualizations of the offer data in certain scenarios

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import plotly.express as px
from dash.dependencies import Input, Output
from datetime import date
import pandas as pd
from app.variables import variables
from dash.exceptions import PreventUpdate

def get_inputs():
    inputs = []
    for col in drops:
        inputs.append(Input(str(col), 'value'))
    return inputs +[Input('totalization','value')]

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
table['oferta'] = table['oferta'].astype('int')

drops = ['linea', 'numero_bus','nodo']

filtered_tables = {
    '0' : table.groupby(['range_hour', 'linea', 'numero_bus','nodo'])['oferta'].sum().to_frame().reset_index(),
    '1' : table.groupby(['dia', 'linea', 'numero_bus','nodo'])['oferta'].sum().to_frame().reset_index(),
    '2' : table.groupby(['val_week', 'linea', 'numero_bus','nodo'])['oferta'].sum().to_frame().reset_index(),
    '3' : table.groupby(['mes', 'linea','numero_bus','nodo'])['oferta'].sum().to_frame().reset_index(),
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
                    {"label": "Time slots", "value": 0},
                    {"label": "Days", "value": 1},
                    {"label": "weeks", "value": 2},
                    {"label": "Months", "value": 3},
                ],
                value=0,
                id="totalization",
                inline=True,
            ),
        ])
    ]
    #Filters
    +get_forms(table),
    
    body=True,
)


app1.layout = dbc.Container(
    [
        html.H1("Offer inquiry"),
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

    data = filtered_tables[str(columns[-1])][(filtered_tables[str(columns[-1])][drops[0]].isin(columns[0])) &
                            (filtered_tables[str(columns[-1])][drops[1]].isin(columns[1])) &
                            (filtered_tables[str(columns[-1])][drops[2]].isin(columns[2]))
                            ]
    
    if len(columns[0]) < 4: 
        if columns[-1] == 0:
            fig = px.bar(data, x='range_hour', y='oferta', color='numero_bus', facet_row="linea", )
        elif columns[-1] == 1:
            fig = px.bar(data, x='dia', y='oferta', color='numero_bus', facet_row="linea", )
        elif columns[-1] == 2:
            fig = px.bar(data, x='val_week', y='oferta', color='numero_bus', facet_row="linea", )
        elif columns[-1] == 3:
            fig = px.bar(data, x='mes', y='oferta', color='numero_bus', facet_row="linea", )
    else:
        if columns[-1] == 0:
            fig = px.bar(data, x='range_hour', y='oferta', color='numero_bus', hover_data=['linea'] )
        elif columns[-1] == 1:
            fig = px.bar(data, x='dia', y='oferta', color='numero_bus', hover_data=['linea'] )
        elif columns[-1] == 2:
            fig = px.bar(data, x='val_week', y='oferta', color='numero_bus', hover_data=['linea'] )
        elif columns[-1] == 3:
            fig = px.bar(data, x='mes', y='oferta', color='numero_bus', hover_data=['linea'])
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    return fig