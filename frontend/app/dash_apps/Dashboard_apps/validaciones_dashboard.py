import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2
from django_plotly_dash import DjangoDash
import plotly.express as px
import dash_bootstrap_components as dbc
from app.variables import variables
import plotly.graph_objects as go


app = DjangoDash('validaciones_dashboard', external_stylesheets=[dbc.themes.BOOTSTRAP])

#df = get_table('validaciones_v2')

df = variables.validaciones
#Promedio mensual de validaciones por hora para distintas paradas
valid_suba_pltmeanparada=df.groupby(['val_hour'])['val_id'].count()
valid_suba_pltmeanparada=valid_suba_pltmeanparada.reset_index()

# promedio mensual de validaciones por hora para distintas linea
valid_suba_pltmeanlinea=df.groupby(['linea', 'val_hour', 'fecha_claring'])['val_id'].count()
valid_suba_pltmeanlinea=valid_suba_pltmeanlinea.reset_index()
valid_suba_pltmeanlinea=valid_suba_pltmeanlinea.groupby(['linea', 'val_hour'])['val_id'].mean().reset_index()

# validaciones totales por día para distintas lineas
valid_suba_pltlinead=df.groupby(['fecha_claring', 'linea'])['val_id'].count()
valid_suba_pltlinead=valid_suba_pltlinead.reset_index()

# validaciones totales por hora para distintas lineas
valid_suba_pltlineah=df.groupby(['val_hour', 'linea'])['val_id'].count()
valid_suba_pltlineah=valid_suba_pltlineah.reset_index()

app.layout = dbc.Container(
    [
        html.Div([
            html.Div([
                html.Div([
                    html.H3(children='Masivo Capital'),
                ], className = 'row'),
                html.Div([
                    dcc.Graph(
                        id='prom_hora',
                        figure = go.Figure(px.bar(valid_suba_pltmeanparada, x="val_hour", y="val_id"))
                        
                    ),
                ], className = 'six columns'),

                # Adding one more app/component
                html.Div([
                    dcc.Graph(
                        id='prom_lineas',
                        figure=px.line(valid_suba_pltmeanlinea, x="val_hour", y="val_id", color='linea'),
                    )
                ], className = 'six columns'),

                html.Div([
                    dcc.Graph(
                        id='prom_dia_linea',
                        figure=px.line(valid_suba_pltlinead, x="fecha_claring", y="val_id", color='linea'),
                    ),
                ], className = 'six columns'),
                
                html.Div([
                    dcc.Graph(
                        id='prom_hora_linea',
                        figure=px.line(valid_suba_pltlineah, x="val_hour", y="val_id", color='linea'),
                    )
                ], className = 'six columns')
        ])
    ])],
fluid = True
)