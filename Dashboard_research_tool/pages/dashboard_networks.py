# ****************************************************************************************** LOCAL
# added for local server
# extra regel om environmental variable te bepalen
# ******************************************************************************************  end local
# import modules
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
from dash import Dash, dcc, html, Input, Output, ctx, ALL, callback, State
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

            html.P('Enter depth: '), dcc.Input(id='depth-input', type='number', placeholder='Enter network depth'),
            html.Br(),
            html.Br(),
            html.P('Enter person name or ID: '), dcc.Input(id='person-input', placeholder='Enter person name or ID'),
            html.Br(),
            html.Br(),
            html.P('Choose network layout: '), dbc.Select(
                id="network-layout-dropdown",
                options=[
                    {"label": "Generational view", "value": "Generational view"},
                    {"label": "Kamada-Kawai layout", "value": "Kamada-Kawai layout"},
                    {"label": "Circular layout", "value": "Circular layout"},
                    # {"label": "Spectral layout", "value": "Spectral layout"},
                ],
                ),
            html.Br(),
            html.Br(),
            html.P("Select relation types to show:"),
            dbc.Checklist(
                options=[
                    {"label": "Vader", "value": "vader"},
                    {"label": "Moeder", "value": "moeder"},
                    {"label": "Huwelijk", "value": "huwelijk"},
                    {"label": "Overleden", "value": "Overleden"}
                ],
                value=[1],
                id="switches-input-network-drawing",
                switch=True,
            ),
            html.Br(),
            html.Br(),
            dbc.Button('Generate Network', id='network-button'),


        ]),
        dbc.Col([
            html.Br(),
            dbc.Button("Additional information", id='relations-modal'),

            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("General Information")),
                    # TODO update as needed
                    dbc.ModalBody("This application can be used to visualise connections between people that lived in Leiden between 1811 and 1995. "
                                  "The networks are generated using birth certificates, death certificates and marriage certificates. "
                                  "To generate a network, choose a person to start looking for connections to that person. For each connection, "
                                  "more connections will be searched for until the specified depth is reached. "
                                  "Keep in mind that higher depths (>3) can take long, this will be improved in the future."),
                    dbc.ModalHeader(dbc.ModalTitle("Layouts")),
                    dbc.ModalBody("There are several layouts available in this application. "),
                    dbc.ModalBody(html.Ul([
                            html.Li("Generational view (recommended): This layout uses layers for each generation. Parents will always be one layer above children, and partners will be on the same layer."),
                            html.Li("Kamada-Kawai layout: This layout attempts to group nodes together using the Kamada–Kawai algorithm."),
                            html.Li("Circular layout: This layout presents all nodes in a circular pattern."),
                        ])
                    ),
                    dbc.ModalHeader(dbc.ModalTitle("Relations examples")),
                    dbc.ModalBody(html.Img(src='assets/network-legenda.png', style={
                        'height': '70%'
                    }),),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id='networks-modal',
                size="xl",
                is_open=False
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Spinner(html.Div(id="loading-output", children=[html.Div(children=[], id='network-div')])),
        ])
    ])],
    fluid=True)


@callback(
    Output("networks-modal", "is_open"),
    [Input("relations-modal", "n_clicks"), Input("close", "n_clicks")],
    [State("networks-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@callback(
    Output('network-div', 'children'),
    # Output('network-visdcc', 'children'),
    Input('network-button', 'n_clicks'),
    Input('depth-input', 'value'),
    Input('person-input', 'value'),
    Input('network-layout-dropdown', 'value'),
    Input('switches-input-network-drawing', 'value')
)
def network(network_button, depth, start_person, layout, drawing_options):
    if ctx.triggered_id == 'network-button':
        fig = figures.create_network_fig(depth, start_person, layout, drawing_options)
        if type(fig) == str:
            return fig
        else:
            return dcc.Graph(figure=fig)
