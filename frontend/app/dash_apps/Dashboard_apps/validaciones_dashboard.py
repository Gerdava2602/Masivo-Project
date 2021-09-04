#A Dash app that displays important plots about the 'validaciones' data

import dash_core_components as dcc
import dash_html_components as html
import psycopg2
from django_plotly_dash import DjangoDash
import plotly.express as px
import dash_bootstrap_components as dbc
from app.variables import variables
import plotly.graph_objects as go


app = DjangoDash('validaciones_dashboard', external_stylesheets=[dbc.themes.BOOTSTRAP])


df = variables.validaciones

#Promedio mensual de validaciones por hora para distintas paradas
valid_suba_pltmeanparada=df.groupby(['range_hour'])['demanda'].sum()
valid_suba_pltmeanparada=valid_suba_pltmeanparada.reset_index()

# promedio diario de validaciones por dia para distintas linea 
valid_suba_pltmeanlinea=df.groupby(['linea_sae', 'val_day'])['demanda'].sum()
valid_suba_pltmeanlinea=valid_suba_pltmeanlinea.reset_index()
valid_suba_pltmeanlinea=valid_suba_pltmeanlinea.groupby(['linea_sae'])['demanda'].mean().reset_index()

# validaciones totales por día para distintas lineas
valid_suba_pltlinead=df.groupby(['fecha_clearing', 'linea_sae'])['demanda'].sum()
valid_suba_pltlinead=valid_suba_pltlinead.reset_index()

# validaciones totales por dia para distintas rutas
valid_suba_pltlineah=df.groupby(['val_day', 'ruta_modificada'])['demanda'].sum()
valid_suba_pltlineah=valid_suba_pltlineah.reset_index()

fig = px.bar(valid_suba_pltmeanparada, x="range_hour", y="demanda")
fig.update_xaxes(tickangle=90)

app.layout = dbc.Container(
    [
        html.Div([
            html.Div([
                html.Div([
                    html.H3(children='Average per time slots'),
                ], className = 'row'),
                html.Hr(),
                html.Div([
                    dcc.Graph(
                        id='prom_hora',
                        figure = fig
                        
                    ),
                ], className = 'six columns'),

                # Adding one more app/component
                html.Div([
                    html.H3(children='Day average per line'),
                ], className = 'row'),
                html.Div([
                    dcc.Graph(
                        id='prom_lineas',
                        figure=px.bar(valid_suba_pltmeanlinea, x="linea_sae", y="demanda", color='linea_sae'),
                    )
                ], className = 'six columns'),

                html.Div([
                    html.H3(children='Daily average'),
                ], className = 'row'),
                html.Hr(),
                html.Div([
                    dcc.Graph(
                        id='prom_dia_linea',
                        figure=px.line(valid_suba_pltlinead, x="fecha_clearing", y="demanda", color='linea_sae'),
                    ),
                ], className = 'six columns'),
                
                html.Div([
                    html.H3(children='Total validations per day for the routes'),
                ], className = 'row'),
                html.Div([
                    dcc.Graph(
                        id='prom_hora_linea',
                        figure=px.bar(valid_suba_pltlineah, x="ruta_modificada", y="demanda", color = 'ruta_modificada'),
                    )
                ], className = 'six columns')
        ])
    ])],
fluid = True
)