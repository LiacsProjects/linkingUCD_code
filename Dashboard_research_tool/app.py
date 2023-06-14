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


# ******************************************************************************************  LOCAL
# Configurate dash application voor DASH
app = Dash(__name__, suppress_callback_exceptions=True,
           routes_pathname_prefix='/',
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           use_pages=True,
           )

# ****************************************************************************************** SERVER
# Configurate dash application voor server
# server = app.server

# ******************************************************************************************  START

app.layout = html.Div([
    dash.page_container
])

# ******************************************************************************************  LOCAL
if __name__ == '__main__':
    app.run_server(port=8050, debug=False)
    #
# ******************************************************************************************  SERVER
# if __name__ == '__main__':
#    app.run_server(debug=False)
#
# ******************************************************************************************  END
