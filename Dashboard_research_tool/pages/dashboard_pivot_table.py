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
                        html.P("Aggregate Function:"),
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
                         # dbc.Button('Random',
                         #            id='random-button'),
                         dbc.Button('Clear',
                                    id='clear-button'),
                         dbc.Button('Additional Information',
                                    id='info-button')]
                        # size='me', #className="d-grid gap-2"
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("General Information")),
                            # TODO update as needed
                            dbc.ModalBody("This application is used to visualize the data present in our database. "
                                          "The database contains data on members from Leiden University, since the sixteenth century. "
                                          "In this application you can interactively generate your own visualizations based on what you want to see. "
                                          "This is done using the dropdown menus and filters. In the following sections the options present in this application are explained."),
                            dbc.ModalHeader(dbc.ModalTitle("Pivot Tables")),
                            dbc.ModalBody("The pivot tables are used to transform non-numeric data into tables and visualisations. "
                                          "The original data will contain columns with data such as a name, place and gender connected to one person. "),
                            dbc.ModalBody(html.B("Index")),
                            dbc.ModalBody("The index of a pivot table take columns from the original data, and displays them in the index of the final table. "),
                            dbc.ModalBody(html.B("Columns")),
                            dbc.ModalBody("The columns in a pivot table take columns from the original data, and displays them in the columns of the final table. "),
                            dbc.ModalBody(html.B("Values")),
                            dbc.ModalBody("The values of a pivot table are what is shown in the cells. The values are columns from the original data that the aggregate function is applied to. "),
                            dbc.ModalBody(html.B("Aggregate Function")),
                            dbc.ModalBody("The aggregate function decides what is done with the data collected by the previous settings. Currently the data only supports the 'count' function.  "),
                            dbc.ModalBody(html.B("Chart Type")),
                            dbc.ModalBody("The Chart Type decides what kind of chart the final visualization will be. "),
                            dbc.ModalBody(html.B("Filters")),
                            dbc.ModalBody("By excluding or only including some data, you can visualize the data that is relevant to the visualization. "
                                          "This is done by entering a value that you want to include or exclude. If you want to enter multiple values you can separate them with "
                                          "a semi-colon, e.g. Country: Nederland;Duitsland;Verenigd Koninkrijk"),
                            dbc.ModalHeader(dbc.ModalTitle("Examples")),
                            dbc.ModalBody(html.B("Example 1")),
                            dbc.ModalBody("A common option is to use 'Type of Person' as values. This effectively means everyone in the database. "
                                          "You can then use filters to choose if you want to view students or professors. "
                                          "This pivot table can be read as follows: 'There were 39 rows with any TypeOfPerson associated with the Archeologie faculty'."),
                            dbc.ModalBody(html.Ul([
                                    html.Li("Index: TypeOfFaculty"),
                                    html.Li("Values: TypeOfPerson"),
                                    html.Li("Columns: -"),
                                    html.Li("Aggregate Function: count"),
                                    html.Li("Chart Type: bar"),
                            ])),
                            dbc.ModalBody(html.Img(src='assets/example_1_table.png', style={
                                'height': '70%'
                            }),),
                            dbc.ModalBody(html.Img(src='assets/example_1_chart.png', style={
                                'width': '80%'
                            }), ),
                            dbc.ModalBody(html.B("Example 2")),
                            dbc.ModalBody("In this example a column was added to visualize the separation between genders. "
                                          "You can also add multiple columns and indexes to further divide the data into separate categories. "
                                          "This pivot table can be read as follows: 'There were 48 men with any TypeOfPerson from the country België, and there were 2 women with the same values and country'. "
                                          "Note that this example only includes professors. Because the students data do not include gender, they are left out automatically with this selection. "),
                            dbc.ModalBody(html.Ul([
                                html.Li("Index: Nationality"),
                                html.Li("Values: TypeOfPerson"),
                                html.Li("Columns: Gender"),
                                html.Li("Aggregate Function: count"),
                                html.Li("Chart Type: bar"),
                            ])),
                            dbc.ModalBody(html.Img(src='assets/example_2_table.png', style={
                                'height': '70%'
                            }), ),
                            dbc.ModalBody(html.Img(src='assets/example_2_chart.png', style={
                                'width': '80%'
                            }), ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Close", id="close", className="ms-auto", n_clicks=0
                                )
                            ),
                        ],
                        id='pivottable-modal',
                        size="xl",
                        is_open=False
                    )
                ]))),
            html.Br(),
            dbc.Row(dbc.Col(
                dbc.Spinner(children=[
                    html.Div(id='pivot-table', children=[], style={
                        'overflow-x': 'auto',
                        'overflow-y': 'auto',
                        'max-height': '500px',
                    })
                    ]
                )
            )
            ),
            dbc.Row(
                dbc.Spinner(children=[html.Div(id='pivot-chart', children=[])])
            )
    ], fluid=True)


@callback(
    Output("pivottable-modal", "is_open"),
    [Input("info-button", "n_clicks"), Input("close", "n_clicks")],
    [State("pivottable-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


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
    # Input('random-button', 'n_clicks'),
    Input('clear-button', 'n_clicks')
)
def extra_buttons(example_button, clear_button):
    if ctx.triggered_id == 'example-button':
        return ['LastName'], ['Gender'], ['Country'], ['Count'], 'bar'

    # if ctx.triggered_id == 'random-button':
    #     return [pivot_table_options[random.randint(0, len(pivot_table_options) - 1)]], \
    #         [pivot_table_options[random.randint(0, len(pivot_table_options) - 1)]], \
    #         [pivot_table_options[random.randint(0, len(pivot_table_options) - 1)]], \
    #         ['Count'], \
    #         graph_options[random.randint(0, len(graph_options) - 1)]

    if ctx.triggered_id == 'clear-button':
        return None, None, None, None, None

# TODO typeof... veranderen van nummers naar categorie
