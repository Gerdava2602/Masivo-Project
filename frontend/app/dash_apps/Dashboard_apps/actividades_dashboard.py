#A Dash app that displays important plots about the 'actividades' data

import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2
from django_plotly_dash import DjangoDash
import plotly.express as px
import dash_bootstrap_components as dbc
from app.variables import variables
import plotly.graph_objects as go


app = DjangoDash('actividades_dashboard', external_stylesheets=[dbc.themes.BOOTSTRAP])

df = variables.oferta
#Promedio mensual de validaciones por hora para distintas paradas
actividades_hora = df.groupby(by=['hora' , 'fecha'])['oferta'].sum().to_frame().reset_index().groupby(['hora']).mean().reset_index()

# promedio mensual de actividades por día
actividades_dia = df.groupby(by=['mes' , 'dia'])['oferta'].sum().to_frame().reset_index().groupby(['dia'])['oferta'].mean().reset_index()

# validaciones totales por día para distintas lineas
actividades_mes=df.groupby(by=['mes'])['oferta'].sum().to_frame().reset_index()
# promedio mensual por día de la semana
actividades_mes_diasemana=df.groupby(by=['dia_semana','mes'])['oferta'].sum().to_frame().reset_index().groupby(['dia_semana'])['oferta'].mean().to_frame().reset_index()

app.layout = dbc.Container(
    [
        html.Div([
            html.Div([
                html.Div([
                    html.H3(children='Average per hour'),
                ], className = 'row'),
                html.Hr(),
                html.Div([
                    dcc.Graph(
                        id='prom_hora',
                        figure = go.Figure(px.bar(actividades_hora, x="hora", y="oferta"))
                        
                    ),
                ], className = 'six columns'),

                # Adding one more app/component
                html.Div([
                    html.H3(children='Average per day'),
                ], className = 'row'),
                html.Hr(),
                html.Div([
                    dcc.Graph(
                        id='prom_día',
                        figure=px.bar(actividades_dia, x="dia", y="oferta"),
                    )
                ], className = 'six columns'),
                
                html.Div([
                    html.H3(children='Monthly average'),
                ], className = 'row'),
                html.Hr(),
                html.Div([
                    dcc.Graph(
                        id='prom_mes',
                        figure=px.bar(actividades_mes, x="mes", y="oferta"),
                    ),
                ], className = 'six columns'),
                
                html.Div([
                    html.H3(children='Average per day of week'),
                ], className = 'row'),
                html.Hr(),
                html.Div([
                    dcc.Graph(
                        id='prom_hora_linea',
                        figure=px.bar(actividades_mes_diasemana, x="dia_semana", y="oferta"),
                    )
                ], className = 'six columns')
        ])
    ])],
fluid = True
)