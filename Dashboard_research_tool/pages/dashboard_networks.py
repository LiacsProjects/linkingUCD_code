# ****************************************************************************************** LOCAL
# added for local server
# extra regel om environmental variable te bepalen
# ******************************************************************************************  end local
# import modules
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
from dash import Dash, dcc, html, Input, Output, ctx, ALL
import figures
import random
import visdcc
import dash


dash.register_page(__name__)

layout = dbc.Container(children=[],
    fluid=True)
