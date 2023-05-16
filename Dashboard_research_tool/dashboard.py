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
import figures

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

# ******************************************************************************************  START

pivot_table_options = ['LastName', 'Gender', 'Nationality', 'Religion', 'Status', 'TypeOfProfession']
app.layout = dbc.Container(children=[
    html.Div(id="p_pivot_table_select", className="container", children=[
        html.Div(children=[
            html.P("Index:"),
            dcc.Dropdown(pivot_table_options,
                         placeholder='Choose values', clearable=False, multi=True, optionHeight=50,
                         id='pivot_index_dropdown', className='dropdown',
                         style={"width": "400px"}),
            html.P("Values:"),
            dcc.Dropdown(pivot_table_options,
                         placeholder='Choose values', clearable=False, multi=True, optionHeight=50,
                         id='pivot_values_dropdown', className='dropdown',
                         style={"width": "400px"}),
            html.P("Columns:"),
            dcc.Dropdown(pivot_table_options,
                         placeholder='Choose values', clearable=False, multi=True, optionHeight=50,
                         id='pivot_columns_dropdown', className='dropdown',
                         style={"width": "400px"}),
            # html.P("Filters:"),
            html.P("AggFunc:"),
            dcc.Dropdown(['Count', 'Sum', 'Mean'],
                         placeholder='Choose values', clearable=False, multi=True, optionHeight=50,
                         id='pivot_aggfunc_dropdown', className='dropdown',
                         style={"width": "400px"}),
            html.Br(),
            html.Br(),
            # html.H1("Chart options:"),
            html.P("Chart type"),
            dcc.Dropdown(['bar', 'line', 'barh', 'hist', 'box', 'area', 'scatter'],
                         placeholder='Choose values', clearable=False, multi=False, optionHeight=50,
                         id='pivot_graph_type_dropdown', className='dropdown',
                         style={"width": "400px"}),
            html.Button(
                'CREATE PIVOT TABLE',
                id='pivot-table-button',
                className='inline',
                style={'font-weight': 'bold', 'margin-left': '20%', 'height': '75px', 'width': '200px'},
            ),
        ]),
        html.Br(),
        html.Div(id='pivot-table', children=[], style={
            'overflow-x': 'auto',
            'overflow-y': 'auto',
            'max-height': '500px',
        }),
        html.Div(id='pivot-chart', children=[])
    ])],
    fluid=True)


@app.callback(
    Output('pivot-table', 'children'),
    Output('pivot-chart', 'children'),

    Input('pivot-table-button', 'n_clicks'),
    [Input("pivot_values_dropdown", 'value')],
    [Input("pivot_columns_dropdown", 'value')],
    [Input("pivot_index_dropdown", 'value')],
    Input("pivot_aggfunc_dropdown", 'value'),
    Input('pivot_graph_type_dropdown', 'value')
)
def pivot_table(pivot_button, pivot_table_values, pivot_table_columns, pivot_table_index, pivot_table_aggfunc,
                pivot_graph_type):
    if ctx.triggered_id == 'pivot-table-button':
        dash_pivot_table, dash_pivot_chart = figures.create_pivot_table(pivot_table_values,
                                                                        pivot_table_columns, pivot_table_index,
                                                                        pivot_table_aggfunc, pivot_graph_type)
        return dash_pivot_table, dash_pivot_chart
    else:
        return None, None

    # TODO animatie kaart
    # TODO gemiddelde leeftijd enz weergeven (ook op een kaart)
    # TODO filters!!
    # TODO ELO integratie met tijmen zn ding, komt via openarchives in michael database



# ******************************************************************************************  LOCAL
if __name__ == '__main__':
    app.run_server(port=8050, debug=False)
    #
# ******************************************************************************************  SERVER
# if __name__ == '__main__':
#    app.run_server(debug=False)
#
# ******************************************************************************************  END
