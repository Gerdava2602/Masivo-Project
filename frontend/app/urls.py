# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views
from app.dash_apps.Dashboard_apps import prueba
from app.dash_apps.Dashboard_apps import oferta_app
from app.dash_apps.registros_apps import actividades_table
from app.dash_apps.registros_apps import demanda_table
from app.dash_apps.Maps_apps import map_dash
from app.dash_apps.Dashboard_apps import validaciones_dashboard
from app.dash_apps.predicciones_apps import demanda_model
from app.dash_apps.Dashboard_apps import actividades_dashboard
from app.dash_apps.predicciones_apps import oferta_model

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    
    re_path(r'.*.html', views.pages, name='pages'),

]
