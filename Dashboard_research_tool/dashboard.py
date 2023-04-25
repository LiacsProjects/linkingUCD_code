# ****************************************************************************************** LOCAL
# added for local server
# extra regel om environmental variable te bepalen
import Add_environment_variable
# ******************************************************************************************  end local
# import modules
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, ctx, dash_table, State, ALL

# import data, page lay-outs and functions
import data
# from figures import professorfigures, studentfigures, rectorfigures, introfigures
# from pages import professorvisuals, rectorvisuals, studentvisuals

# Import database class
from Adapters import database

# Parameters and constants
YEAR_STEP = 5
MARK_SPACING = 10
THESIS_COLUMN_NAME = 'Thesis'
SUBJECT_AREA_COLUMN_NAME = 'Subject area'
# ******************************************************************************************  LOCAL
# Configurate dash application voor DASH
app = Dash(__name__, suppress_callback_exceptions=True,
           routes_pathname_prefix='/',
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           #  uitgeschakeld  #      requests_pathname_prefix='/dashboard/'
           )

# ****************************************************************************************** SERVER
# Configurate dash application voor server
# server = app.server

# ******************************************************************************************  TODO

# TODO: implement store functions to allow users to save their changes made to the dashboard TODO:
#  connect database to dashboard
# TODO: create joined page for all persons TODO: link city/country coordinates to city/country dataframes, preferably
#  through function that reads coordinates from a file: countries.geojson and cities1-2-3.csv

# ******************************************************************************************  START
app.layout = dbc.Container(children=[
    html.Div(id='page_top', children=[
        html.Img(id="logo", src="assets/Leiden_zegel.png", n_clicks=0),
        html.H1('Leiden Univercity Project', id="page_title")]),
    dbc.Button("Home", id="btn-home", class_name="me-1", n_clicks=0),
    html.Div(id='page-handler', hidden=True),
], fluid=True)


# ******************************************************************************************  LOCAL
if __name__ == '__main__':
    app.run_server(port=8050, debug=False)
    #
# ******************************************************************************************  SERVER
# if __name__ == '__main__':
#    app.run_server(debug=False)
#
# ******************************************************************************************  END
