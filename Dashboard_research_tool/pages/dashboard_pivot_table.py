# ****************************************************************************************** LOCAL
# added for local server
# extra regel om environmental variable te bepalen
# ******************************************************************************************  end local
# import modules
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
from dash import Dash, dcc, html, Input, Output, ctx, ALL, callback
import figures
import random
import visdcc
import dash


dash.register_page(__name__)

pivot_table_options = ['TypeOfPerson', 'FirstName', 'LastName', 'FamilyName', 'Affix', 'Nickname', 'Gender',
                       'Nationality', 'Religion', 'Status', 'Handles', 'AVG',
                       'TypeOfProfession', 'TypeOfPosition', 'TypeOfExpertise', 'TypeOfFaculty', 'professionStartDate',
                       'professionEndDate',
                       'TypeOfLocation', 'City', 'Country', 'Region', 'ISO_Alpha_3']
graph_options = ['bar', 'line', 'barh', 'hist', 'box', 'area', 'scatter']

layout = dbc.Container(children=[dbc.Row([
                dbc.Col([html.P("Index:"),
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
                        html.P("AggFunc:"),
                        dcc.Dropdown(['Count', 'Sum', 'Mean'],
                                     placeholder='Choose values', clearable=False, multi=True, optionHeight=50,
                                     id='pivot_aggfunc_dropdown', className='dropdown',
                                     style={"width": "400px"}),
                        # html.H1("Chart options:"),
                        html.P("Chart type"),

                        dcc.Dropdown(graph_options,
                                     placeholder='Choose values', clearable=False, multi=False, optionHeight=50,
                                     id='pivot_graph_type_dropdown', className='dropdown',
                                     style={"width": "400px"}),
                        ], width=4),
                dbc.Col([html.P("Filters:"),
                        html.Div(id='filters_group', children=[]), ])
            ]),
            dbc.Row(dbc.Col(
                html.Div(children=[

                    html.Br(),
                    dbc.ButtonGroup(
                        [dbc.Button('Create pivot table',
                                    id='pivot-table-button'),
                         dbc.Button('Load example',
                                    id='example-button'),
                         dbc.Button('Random',
                                    id='random-button'),
                         dbc.Button('Clear',
                                    id='clear-button')],
                        # size='me', #className="d-grid gap-2"
                    ),
                ]))),
            html.Br(),
            dbc.Row(dbc.Col(
                html.Div(id='pivot-table', children=[], style={
                    'overflow-x': 'auto',
                    'overflow-y': 'auto',
                    'max-height': '500px',
                }))),
            dbc.Row(html.Div(id='pivot-chart', children=[]))], fluid=True)


@callback(
    Output('pivot-table', 'children'),
    Output('pivot-chart', 'children'),

    Input('pivot-table-button', 'n_clicks'),
    [Input("pivot_values_dropdown", 'value')],
    [Input("pivot_columns_dropdown", 'value')],
    [Input("pivot_index_dropdown", 'value')],
    Input("pivot_aggfunc_dropdown", 'value'),
    Input('pivot_graph_type_dropdown', 'value'),
    Input({"type": "filter-input", "index": ALL}, "value"),
    Input({"type": "filter-label", "index": ALL}, "children"),
    Input({"type": "filter-exclude", "index": ALL}, "on")
)
def pivot_table(pivot_button, pivot_table_values, pivot_table_columns, pivot_table_index, pivot_table_aggfunc,
                pivot_graph_type, filter_input, filter_labels, filter_exclude):
    if ctx.triggered_id == 'pivot-table-button':
        dash_pivot_table, dash_pivot_chart = figures.create_pivot_table(pivot_table_values,
                                                                        pivot_table_columns, pivot_table_index,
                                                                        pivot_table_aggfunc, pivot_graph_type,
                                                                        filter_input, filter_labels, filter_exclude)
        return dash_pivot_table, dash_pivot_chart
    else:
        return None, None


@callback(
    Output('filters_group', 'children'),
    Input('pivot_values_dropdown', 'value'),
    Input('pivot_columns_dropdown', 'value'),
    Input('pivot_index_dropdown', 'value')
)
def filters(values, columns, index):
    attributes = []
    if values:
        attributes += values
    if columns:
        attributes += columns
    if index:
        attributes += index

    div_children_list = []
    counter = 1
    for attribute in attributes:
        inputgroup = dbc.InputGroup([dbc.InputGroupText(attribute, id={"type": "filter-label", "index": counter}),
                                     dbc.InputGroupText(children=['Exclude ', daq.BooleanSwitch(id={"type": "filter-exclude", "index": counter}, on=False)]),
                                     dbc.Input(id={"type": "filter-input", "index": counter})], style={})
        div_children_list.append(inputgroup)
        div_children_list.append(html.Br())
        counter += 1

    minimum_filter = dbc.InputGroup(
        [dbc.InputGroupText('Minimum threshold', id={"type": "filter-label", "index": counter}),
         dbc.Input(type='number', id={"type": "filter-input", "index": counter})], style={})
    div_children_list.append(minimum_filter)
    div_children_list.append(html.Br())

    maximum_filter = dbc.InputGroup(
        [dbc.InputGroupText('Maximum threshold', id={"type": "filter-label", "index": counter}),
         dbc.Input(type='number', id={"type": "filter-input", "index": counter})], style={})
    div_children_list.append(maximum_filter)
    div_children_list.append(html.Br())

    return div_children_list


@callback(
    Output("pivot_values_dropdown", 'value'),
    Output("pivot_columns_dropdown", 'value'),
    Output("pivot_index_dropdown", 'value'),
    Output("pivot_aggfunc_dropdown", 'value'),
    Output('pivot_graph_type_dropdown', 'value'),
    Input('example-button', 'n_clicks'),
    Input('random-button', 'n_clicks'),
    Input('clear-button', 'n_clicks')
)
def extra_buttons(example_button, random_button, clear_button):
    if ctx.triggered_id == 'example-button':
        return ['LastName'], ['Gender'], ['Country'], ['Count'], 'bar'

    if ctx.triggered_id == 'random-button':
        return [pivot_table_options[random.randint(0, len(pivot_table_options) - 1)]], \
            [pivot_table_options[random.randint(0, len(pivot_table_options) - 1)]], \
            [pivot_table_options[random.randint(0, len(pivot_table_options) - 1)]], \
            ['Count'], \
            graph_options[random.randint(0, len(graph_options) - 1)]

    if ctx.triggered_id == 'clear-button':
        return None, None, None, None, None


@callback(
    Output('network-div', 'children'),
    Input('network-button', 'n_clicks')
)
def network(network_button):
    if ctx.triggered_id == 'network-button':
        network_df = pd.read_csv('../genealogical_visualisation/relations.csv', sep=';')
        linked_person_df = pd.read_csv('../genealogical_visualisation/RL Gelinkte Personen.csv', sep=';')

        print(len(network_df))
        network_df = network_df[:1000]

        node_list = list(set(list(network_df['rel1_id'].unique()) + list(network_df['rel2_id'].unique())))
        name_list = []
        for node in node_list:
            try:
                name_list.append(list(linked_person_df[linked_person_df['uuid'] == node]['name'])[0])
            except IndexError:
                name_list.append("No name found")

        print(node_list[:10])
        print(name_list[:10])

        nodes = [{'id': node_name, 'label':name_list[i], 'shape': 'dot', 'size': '7', 'color':'red'} for i, node_name in enumerate(node_list)]
        # print(nodes)

        edges = []
        for row in network_df.to_dict(orient='records'):
            source, target, type = row['rel1_id'], row['rel2_id'], row['rel_type']

            if type == 'partner':
                edges.append({
                    'id': source + '__' + target,
                    'from': source,
                    'to': target,
                    'width': 2,
                    'color': 'blue'
                })

            elif type == 'zoon':
                edges.append({
                    'id': source + '__' + target,
                    'from': source,
                    'to': target,
                    'width': 2,
                    'color': 'yellow'
                })

            elif type == 'dochter':
                edges.append({
                    'id': source + '__' + target,
                    'from': source,
                    'to': target,
                    'width': 2,
                    'color': 'orange'
                })

        network_vis = visdcc.Network(id='network', data={'nodes': nodes, 'edges': edges},
                                     options=dict(height='600px', width='800px'))


        return network_vis

# TODO animatie kaart
# TODO gemiddelde leeftijd enz weergeven (ook op een kaart)
# TODO ELO integratie met tijmen zn ding, komt via openarchives in michael database
# TODO geografisch
# TODO filters specifiek voor jaartallen/data
# TODO typeof... veranderen van nummers naar categorie
