# ****************************************************************************************** LOCAL
# added for local server
# extra regel om environmental variable te bepalen
# ******************************************************************************************  end local
# import modules
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
from dash import Dash, dcc, html, Input, Output, ctx, ALL, callback, State
import figures
import random
import visdcc
import dash

dash.register_page(__name__)

layout = dbc.Container(children=[dbc.Row([dbc.Col([
    html.Br(),
    html.P("Select data:"),
    dbc.Select(
        id="geo-data-dropdown",
        options=[
            {"label": "Birth Country", "value": "Birth Country"},
            {"label": "Death Country", "value": "Death Country"},
            {"label": "Birth City", "value": "Birth City"},
            {"label": "Death City", "value": "Death City"},
        ],
    ),
    html.Br(),
    html.P('Select type of person:'),
    dbc.Select(
        id="geo-person-dropdown",
        options=[
            {"label": "Professor", "value": "Professor"},
            {"label": "Student", "value": "Student"},
        ],
    ),
    html.Br(),
    html.Div([
        html.P(["Use year filter: ", daq.BooleanSwitch(id='year-bool-switch', on=False)])
    ], style={'display': 'inline-block'}),
    html.Div(children=[html.P('Select year range:'),
                       dcc.RangeSlider(1575, 2025, 25, value=[1575, 2019], id='geo-slider',
                                       marks={i: '{}'.format(i) for i in range(1575, 2019, 25)}),
                       ]),
    html.Br(),
    html.P("Choose scale (only for country maps): "),
    dbc.RadioItems(
            options=[
                {"label": "Log", "value": 'Log'},
                {"label": "Absolute", "value": 'Absolute'},
            ],
            value=1,
            id="geo-scale-radioitems",
        ),
    html.Br(),
    dbc.Button('Create Map', id='map-button'),
    html.Br(),
    ], width=10)]),
    dbc.Col([html.Div([], id='map-div')], width=10),
    ],
    fluid=True)


@callback(
    Output('map-div', 'children'),
    Input('map-button', 'n_clicks'),
    Input('geo-data-dropdown', 'value'),
    Input('geo-person-dropdown', 'value'),
    Input('geo-slider', 'value'),
    Input('year-bool-switch', 'on'),
    Input('geo-scale-radioitems', 'value')
)
def create_map(map_button, data_selection, person_selection, year_selection, year_bool, scale_option):
    if ctx.triggered_id == 'map-button':
        if data_selection == 'Birth City' or data_selection == 'Death City':
            return dcc.Graph(figure=figures.create_city_map(data_selection, person_selection, year_selection, year_bool))
        elif data_selection == 'Birth Country' or data_selection == 'Death Country':
            return dcc.Graph(figure=figures.create_country_map(data_selection, person_selection, year_selection, year_bool, scale_option))

