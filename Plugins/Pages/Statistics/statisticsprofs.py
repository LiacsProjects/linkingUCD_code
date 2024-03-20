#
# Imports
#
import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc

from Plugins.globals import data
from Plugins.globals import SUBJECT_DROPDOWN, DEFAULT_SUBJECT, GRAPH_CONFIG
from Plugins.Data import exceldata as data
from Plugins.Pages.Statistics import statisticsgraphs

#
# Configure dash page
#
dash.register_page(
    __name__,
    title="Statistics Professors",
    description="Visuals for statistical data about professors",
    path="/pages/statistics",
    order=2
)

#
# Layout
#
layout = html.Div(
    id='p_subject_info',
    className='container',
    children=[
        html.Div(id='p_subject_header',
                 className='page_header',
                 children=[html.H1('Professors')]),

        html.Div(id='p-subject-information-container',
                 className='left_container',
                 children=[
                    html.H3('Graph settings:'),
                    dcc.Dropdown(
                        SUBJECT_DROPDOWN,
                        DEFAULT_SUBJECT,
                        placeholder='Choose a field',
                        clearable=False,
                        style={'background-color':
                               'rgba(223,223,218,0.7)',
                               'color': 'black',
                               'margin': '1% 1% 1% 1%'},
                        id='p-subject-dropdown',
                        className='dropdown'
                    ),
                    html.Div(id='p_subject_header2',
                             children=[html.H3('Statistics:'),
                                       html.Div(id='p-subject-information'),
                                       ]
                             ),
                ]),

       html.Div(id='p-subject-dropdown-container', className='right_container',
                children=[
                    html.H3('Graph:'),
                    dcc.Graph(id='p-subject-graph',
                              config=GRAPH_CONFIG,
                             ),
                    html.H3('Statistical data:'),
                    html.Div(id='p-subject-table-container'),
                ]),

    ])

#
# Statistical  information callbacks
#
@callback(
    Output('p-subject-graph', 'figure'),
    Input('p-subject-dropdown', 'value'),
    running=[
        (Output('p-subject-dropdown', 'disabled'), True, False),
    ],
)
def update_subject_output(selected_subject):
    figure = statisticsgraphs.create_subject_info_graph(selected_subject)
    return figure


# Statistictable
@callback(
    Output('p-subject-table-container', 'children'),
    Input('p-subject-dropdown', 'value'),
)
def update_timeline_table(selected_subject):
    df, subject, name = statisticsgraphs.get_variables(selected_subject)
    df = df.rename(columns={subject: name, 'year': 'Year', 'count': 'Appointments', 'century': 'Century'})
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': i, 'name': i, "hideable": "last"} for i in df.columns],
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_size=100,
        fixed_rows={'headers': True},
        style_cell={
            'width': '{}%'.format(len(df.columns)),
            'textOverflow': 'ellipsis',
            'overflow': 'hidden'
        },
        style_table={'overflowY': 'auto', 'overflowX': 'auto'},
        style_header={'backgroundColor': '#001158', 'color': 'white'},
        style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'white', 'color': 'black'},
        virtualization=True,
        #       export/download optie uitgeschakeld
        #       export_format='xlsx',
        #       export_headers='display',
        merge_duplicate_headers=True,
        id='p-subject-table'
    )


# Statistical information
@callback(
    Output('p-subject-information', 'children'),
    Input('p-subject-dropdown', 'value'),
    Input('p-subject-graph', 'hoverData'),
)
def update_timeline_information(selected_subject, hover_data):
    if hover_data is not None:
        text = hover_data['points'][0]['hovertext']
    else:
        text = None
    df, subject, name = statisticsgraphs.get_variables(selected_subject)
    total = df['count'].sum()
    fraction = df.loc[df[subject] == text, 'count'].sum()
    percentage = round(fraction / total * 100, 2)
    if subject == 'year':
        return html.Div(id='p-subject-hover-info', children=[
            html.Table(id='p-subject-table', children=[
                html.Tr(children=[
                    html.Td('Field'),
                    html.Td(selected_subject),
                ]),
                html.Tr(children=[
                    html.Td(str(name) + ' amount'),
                    html.Td(df[subject].nunique()),
                ]),
                html.Tr(children=[
                    html.Td(f'Total {subject}s'),
                    html.Td(total),
                ]),
                html.Tr(children=[
                    html.Td('Average appointments per year'),
                    html.Td(html.Td(round(df['count'].mean(), 0))),
                ]),
                html.Tr(children=[
                    html.Td('Year with most appointments'),
                    html.Td(df.loc[df['count'] == df['count'].max(), subject].unique()),
                ]),
                html.Tr(children=[
                    html.Td('Year with least appointments'),
                    html.Td(df.loc[df['count'] == df['count'].min(), subject].unique()),
                ]),
            ]),
            html.Br(),
            html.Table(id='p-chosen-subject-table', children=[
                html.Tr(children=[
                    html.Td('Year'),
                    html.Td(text),
                ]),
                html.Tr(children=[
                    html.Td('Nr professors  '),
                    html.Td(fraction),
                ]),
                html.Tr(children=[
                    html.Td('Percentage'),
                    html.Td(percentage),
                ]),
            ]),
            html.Br(),
            html.Div(id='p-century-table'),
        ])
    else:
        return html.Div(id='p-subject-hover-info', children=[
            html.Table(id='p-subject-table', children=[
                html.Tr(children=[
                    html.Td('Field'),
                    html.Td(selected_subject),
                ]),
                html.Tr(children=[
                    html.Td(str(name) + ' amount'),
                    html.Td(df[subject].nunique()),
                ]),
                html.Tr(children=[
                    html.Td(f'Total {subject}s'),
                    html.Td(total),
                ]),
                html.Tr(children=[
                    html.Td('Average yearly appointments per ' + str(subject)),
                    html.Td(html.Td(round(df['count'].mean(), 0))),
                ]),
                html.Tr(children=[
                    html.Td(str(name) + ' with most appointments in one year'),
                    html.Td(df.loc[df['count'] == df['count'].max(), subject].unique()),
                ]),
                html.Tr(children=[
                    html.Td(str(name) + ' with least appointments in one year'),
                    html.Td(df.loc[df['count'] == df['count'].min(), subject].unique()[0]),
                ]),
            ]),
            html.Br(),
            html.Table(id='p-chosen-subject-table', children=[
                html.Tr(children=[
                    html.Th(name),
                    html.Th(text),
                ]),
                html.Tr(children=[
                    html.Td('Nr professors  '),
                    html.Td(fraction),
                ]),
                html.Tr(children=[
                    html.Td('Percentage'),
                    html.Td(percentage),
                ]),
            ]),
            html.Br(),
            html.Div(id='p-century-table'),
        ])


#
# Statistical information table
#
@callback(
    Output('p-subject-table', 'children'),
    Input('p-subject-dropdown', 'value'),
)
def update_timeline_table(selected_subject):
    df, subject, name = statisticsgraphs.get_variables(selected_subject)
    table_df = statisticsgraphs.create_century_table(df, name)
    return dash_table.DataTable(
        data=table_df.to_dict('records'),
        columns=[{'id': i, 'name': i} for i in table_df.columns],
        fixed_rows={'headers': True},
        style_cell={
            'width': '{}%'.format(len(df.columns)),
            'textOverflow': 'ellipsis',
            'overflow': 'hidden'
        },
        style_header={'backgroundColor': '#001158', 'color': 'white'},
        style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'white', 'color': 'black'},
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Statistic} = "Century"',
                },
                'backgroundColor': 'white',
                'color': 'black',
            }],
        virtualization=True,
        id='p-subject-information-table',
    )
