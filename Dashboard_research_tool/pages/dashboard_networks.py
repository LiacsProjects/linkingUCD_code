# ****************************************************************************************** LOCAL
# added for local server
# extra regel om environmental variable te bepalen
# ******************************************************************************************  end local
# import modules
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
from dash import Dash, dcc, html, Input, Output, ctx, ALL, callback
# import figures
import random
import visdcc
import dash
import networkx as nx
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import time
import figures

dash.register_page(__name__)

layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            # html.Div(children=[
            #     visdcc.Network(id='net', data=dict(), options=dict(height='600px', width='80%'))
            # ], id='network-div'),

            html.P('Enter depth'), dcc.Input(id='depth-input', type='number', placeholder='Enter network depth'),
            html.Br(),
            html.Br(),
            html.P('Enter person'), dcc.Input(id='person-input', type='number', placeholder='Enter person to start search'),
            html.Br(),
            html.Br(),
            dbc.Button('Generate Network', id='network-button'),
            html.Div(children=[], id='network-div'),
            html.Div(children=[], id='network-visdcc')

        ])
    ])],
    fluid=True)

@callback(
    Output('network-div', 'children'),
    # Output('network-visdcc', 'children'),
    Input('network-button', 'n_clicks'),
    Input('depth-input', 'value'),
    Input('person-input', 'value'),
)
def network(network_button, depth, start_person):
    if ctx.triggered_id == 'network-button':

        fig = figures.create_network_fig(depth, start_person)
        return dcc.Graph(figure=fig)
