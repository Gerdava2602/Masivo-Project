# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views
from app.dash_apps.predicciones_apps import simpleexample
from app.dash_apps.predicciones_apps import example2
from app.dash_apps.predicciones_apps import prueba
from app.dash_apps.registros_apps import validaciones_table
from app.dash_apps.registros_apps import localizacion_table
from app.dash_apps.registros_apps import demanda_table
from app.dash_apps.Maps_apps import map_dash
from app.dash_apps.Dashboard_apps import validaciones_dashboard

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    
    re_path(r'.*.html', views.pages, name='pages'),

]
