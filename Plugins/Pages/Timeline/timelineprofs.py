#
# Set environment base path
#
ON_SERVER = False
if not ON_SERVER:
    # added for local server
    # extra regel om environmental variable te bepalen
    # voor server draaien dashboard.wsgi ?
    from Plugins import add_environment_variable

#
# Imports
#
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

from Plugins.Data import exceldata as data
from Plugins.Pages.Timeline import timelinegraphs as professorfigures

#
# Configure dash page
#
dash.register_page(
    __name__,
    title="Timeline Professors",
    description="Visuals for aggregated temporal data about professors",
    path="/pages/timeline",
    order=0
)

#
# Global constants
#
CENTURY_STEP = 1
YEAR_STEP = 5
MARK_SPACING = 10
START_CENTURY = 16

DEFAULT_SUBJECT = 'Appointment'
SUBJECT_DROPDOWN = ['Gender', 'Birth', 'Birth place', 'Birth country', 'Death', 'Death place',
                    'Death country', 'Promotion', 'Promotion type', 'Promotion place', 'Appointment',
                    'Job', 'Subject area', 'Faculty', 'End of employment']

DEFAULT_GRAPH_SUBJECT = 'Appointment'
GRAPH_SUBJECT_DROPDOWN = ['Gender', 'Birth', 'Death', 'Promotion', 'Promotion type', 'Appointment',
                          'Job', 'Subject area', 'Faculty', 'End of employment']

DEFAULT_GRAPH = 'Bar graph'
GRAPH_DROPDOWN = ['Bar graph', 'Line graph', 'Scatter graph']
GRAPH_CONFIG = {'modeBarButtonsToRemove': ['toImage'], 'displayModeBar': True,}

#
# Global vars
#
current_century = data.all_dates_df[(data.all_dates_df['century'] <= START_CENTURY)]

years = []
for y in current_century['year'][0::YEAR_STEP]:
    years.append(y)
years.append(current_century['year'].max())

#
# Layout page
#
layout = html.Div(
    id='p_timeline',
    className='container',
    children=[

        html.Div(
            id='p_timeline_header',
            className='page_header',
            children=[html.H1('Professors')]),

        html.Div(
            id='p_inputs',
            className='left_container',
            children=[

                html.H3('Graph settings:'),
                html.P('Select Subject:'),
                dcc.Dropdown(SUBJECT_DROPDOWN, DEFAULT_SUBJECT,
                             placeholder='Choose a subject:',
                             clearable=False,
                             id='p-year-century-subject-dropdown', className='dropdown'),

                html.P('Select century range:'),
                dcc.RangeSlider(
                         data.all_dates_df['century'].min(),
                         data.all_dates_df['century'].max(),
                         CENTURY_STEP,
                         value=[data.year_df['century'].min(),
                                data.all_dates_df['century'].min()],
                         marks={str(cent): str(cent) for cent in data.all_dates_df['century']},
                         id='p-year-century-slider',
                ),

                html.P('Select year range:'),
                dcc.RangeSlider(
                     current_century['year'].min(),
                     current_century['year'].max(),
                     YEAR_STEP,
                     id='p-year-slider',
                ),

                html.Div(
                    id='p-year-slider-container'),
                    html.P('Select graph type:'),
                    dcc.Dropdown(
                        GRAPH_DROPDOWN,
                        DEFAULT_GRAPH,
                        placeholder='Choose a graph style',
                        clearable=False,
                        id='p-year-century-dropdown',
                        className='dropdown'
                    ),

                html.Div(id='p-year-century-graph'),],),

        html.Div(
            id='p-year-century-dropdown-container',
            className='right_container',
            children=[
                html.H4('Graph:'),
                dcc.Graph(id='p-year-century-graph',
                          config=GRAPH_CONFIG, )
                ],
            ),

        html.Div(
            id='p-timeline-information-container',
            className='left_container ',
            children=[
                  html.H3('Information:'),
                  html.Div(id='p-timeline-information'),]
            ),

        html.Div(
            id='p-century-dropdown-container',
            className='right_container',
            children=[
                  html.H4('Sorted bar graph:'),
                  dcc.Graph(id='p-century-graph',
                            config=GRAPH_CONFIG,),
                  ]
            ), ])

#
# Year slider
#
@callback(
    Output('p-year-slider', 'min'),
    Output('p-year-slider', 'max'),
    Output('p-year-slider', 'value'),
    Output('p-year-slider', 'marks'),
    Input('p-year-century-slider', 'value')
)

def update_year_slider(century):
    current_century = data.all_dates_df[(data.all_dates_df['century'] <= century[-1])]
    current_century = current_century[(current_century['century'] >= century[0])]
    years = []
    for y in current_century['year'][0::YEAR_STEP]:
        years.append(y)
    years.append(current_century['year'].max())
    min_year = current_century['year'].min()
    max_year = current_century['year'].max()
    value = [min_year, max_year]
    marks: dict = {str(year): str(year) for year in
                   range(min_year, max_year, int((max_year - min_year) / MARK_SPACING))}
    return min_year, max_year, value, marks

#
# Year-Century graph
#
@callback(
    Output('p-year-century-graph', 'figure'),
    Input('p-year-century-subject-dropdown', 'value'),
    Input('p-year-century-slider', 'value'),
    Input('p-year-slider', 'value'),
    Input('p-year-century-dropdown', 'value'),
    running=[
        (Output('p-year-century-subject-dropdown', 'disabled'), True, False),
    ],
)
def update_year_century_output(selected_subject, selected_century, selected_year, selected_dropdown):
    figure = professorfigures.create_year_cent_figure(
        selected_subject,
        selected_century,
        selected_year,
        selected_dropdown)
    return figure

#
# Century-Graph
#
@callback(
    Output('p-century-graph', 'figure'),
    Input('p-year-century-subject-dropdown', 'value'),
    Input('p-year-century-slider', 'value'),
)
def update_century_output(selected_subject, selected_century):
    figure = professorfigures.create_cent_figure(selected_subject, selected_century)
    return figure

#
# Timeline information
#
@callback(
    Output('p-timeline-information', 'children'),
    Input('p-year-century-subject-dropdown', 'value'),
    Input('p-year-century-graph', 'hoverData'),
    Input('p-year-century-graph', 'figure'),
)
def update_timeline_information(selected_subject, hover_data, figure):
    if hover_data is not None:
        text = hover_data['points'][0]['hovertext']
        y = hover_data['points'][0]['x']
        year = int(y)
    else:
        text = None
        if not 'customdata' in figure['data'][0].keys():
            return
        year = figure['data'][0]['x'][0]

    df, subject, name = professorfigures.get_variables(selected_subject)
    century = df.loc[df['year'] == year, 'century'].values[0]
    enrollments = df.loc[df['year'] == year, 'count'].values[0]
    last_year = year - 1

    if last_year in figure['data'][0]['x']:
        last_year_enrollments = df.loc[df['year'] == last_year, 'count'].values[0]
        growth = enrollments - last_year_enrollments
    else:
        growth = 'No data'

    if subject == 'year':
        return html.Table(id='p-timeline-table', children=[
            html.Tr(children=[
                html.Th('Subject'),
                html.Th(selected_subject),
            ]),
            html.Tr(children=[
                html.Td('Year'),
                html.Td(year),
            ]),
            html.Tr(children=[
                html.Td('Century'),
                html.Td(century),
            ]),
            html.Tr(children=[
                html.Td('Appointments'),
                html.Td(enrollments),
            ]),
            html.Tr(children=[
                html.Td('Yearly Growth'),
                html.Td(growth),
            ]),
            html.Br(),
            html.Tr(children=[
                html.Th('General information'),
            ]),
            html.Tr(children=[
                html.Td('Total appointments'),
                html.Td(df['count'].sum()),
            ]),
            html.Tr(children=[
                html.Td('Most appointments'),
                html.Td(df['count'].max()),
            ]),
            html.Tr(children=[
                html.Td('Year with highest value'),
                html.Td(df.loc[df['count'] == df['count'].max(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Least appointments'),
                html.Td(df['count'].min()),
            ]),
            html.Tr(children=[
                html.Td('Year with lowest value'),
                html.Td(df.loc[df['count'].min(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Average appointments'),
                html.Td(round(df['count'].mean(), 0)),
            ]),
        ]),
    else:
        return html.Table(id='p-timeline-table', children=[
            html.Tr(children=[
                html.Td('Subject:'),
                html.Td(selected_subject),
            ]),
            html.Tr(children=[
                html.Td(name),
                html.Td(text),
            ]),
            html.Tr(children=[
                html.Td('Year'),
                html.Td(year),
            ]),
            html.Tr(children=[
                html.Td('Century'),
                html.Td(century),
            ]),
            html.Tr(children=[
                html.Td('Appointments'),
                html.Td(enrollments),
            ]),
            html.Tr(children=[
                html.Td('Yearly Growth'),
                html.Td(growth),
            ]),
            html.Br(),
            html.Tr(children=[
                html.Th('General information'),
            ]),
            html.Tr(children=[
                html.Td('Total appointments'),
                html.Td(df['count'].sum()),
            ]),
            html.Tr(children=[
                html.Td('Most appointments'),
                html.Td(df['count'].max()),
            ]),
            html.Tr(children=[
                html.Td('Year with highest value'),
                html.Td(df.loc[df['count'] == df['count'].max(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Least appointments'),
                html.Td(df['count'].min()),
            ]),
            html.Tr(children=[
                html.Td('Year with lowest value'),
                html.Td(df.loc[df['count'].min(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Average appointments'),
                html.Td(round(df['count'].mean(), 0)),
            ]),
        ]),
