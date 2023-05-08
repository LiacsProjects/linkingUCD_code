# Creating dataframe
# Import modules
from dash import dcc, html
import data
from figures import rectorfigures

# Parameters and constants
CENTURY_STEP = 1
YEAR_STEP = 5
MARK_SPACING = 10
START_CENTURY = 16
SUBJECT_DROPDOWN = ['Rectors']
DEFAULT_SUBJECT = 'Rectors'
GRAPH_DROPDOWN = ['Bar graph', 'Line graph', 'Scatter graph']
DEFAULT_GRAPH = 'Bar graph'
GRAPH_CONFIG = {'modeBarButtonsToRemove': ['toImage'], 'displayModeBar': True,}

# Data year calculaionss
current_century = data.all_dates_df[(data.all_dates_df['century'] <= START_CENTURY)]
years = []
for y in current_century['year'][0::YEAR_STEP]:
    years.append(y)
years.append(current_century['year'].max())

# layout page 
timeline = html.Div(id='r_timeline', className='container',
                    children=[
                        html.Div(id='r_timeline_header', className='page_header',
                                 children=[html.H1('Rectores Magnifici')]
                                 ),
                        html.Div(id='r_inputs', className='left_container ',
                                 children=[
                                     html.H3('Graph settings:'),
                                     html.P('Select Subject:'),
                                     dcc.Dropdown(
                                         SUBJECT_DROPDOWN,
                                         DEFAULT_SUBJECT,
                                         placeholder='Choose a subject',
                                         clearable=False,
                                         id='r-year-century-subject-dropdown',
                                         className='dropdown'
                                     ),

                                     html.P('Select century range:'),
                                     dcc.RangeSlider(
                                         data.rector_years['century'].min(),
                                         data.rector_years['century'].max(),
                                         CENTURY_STEP,
                                         value=[data.rector_years['century'].min(),
                                                data.rector_years['century'].min()],
                                         marks={str(cent):
                                                str(cent) for cent in data.rector_years['century']},
                                         id='r-year-century-slider'
                                     ),
                                     html.P('Select year range:'),
                                     dcc.RangeSlider(
                                         current_century['year'].min(),
                                         current_century['year'].max(),
                                         YEAR_STEP,
                                         id='r-year-slider',
                                     ),
                                     html.Div(id='r-year-slider-container'),
                                     html.P('Select graph type:'),
                                     dcc.Dropdown(
                                         GRAPH_DROPDOWN, DEFAULT_GRAPH,
                                         placeholder='Choose a graph style',
                                         clearable=False,
                                         id='r-year-century-dropdown',
                                         className='dropdown'
                                     ),
                                 ]
                                 ),
                        html.Div(id='r-year-century-container', className='right_container',
                                 children=[
                                     html.H4('Graph:'),
                                     dcc.Graph(id='r-year-century-graph',
                                               config=GRAPH_CONFIG,
                                               )
                                 ],
                                 ),
                        html.Div(id='r-timeline-information-container', className='left_container',
                                 children=[
                                     html.H3('Information:'),
                                     html.Div(id='r-timeline-information', ),
                                 ]
                                 ),
                        html.Div(id='r-century-graph-container', className='right_container',
                                 children=[
                                     html.H4('Sorted bar graph:'),
                                     dcc.Graph(id='r-century-graph',
                                               config=GRAPH_CONFIG,
                                               )
                                 ],
                                 ),
                    ]),

subject_information = html.Div(id='r_subject_info', className='container',
                               children=[
                                   html.Div(id='r_subject_header', className='page_header',
                                            children=[html.H1('Rectores Magnifici')]),
                                   html.Div(id='r-subject-information-container', className='left_container',
                                            children=[
                                                html.H3('Graph settings:'),
                                                dcc.Dropdown(
                                                    SUBJECT_DROPDOWN,
                                                    DEFAULT_SUBJECT,
                                                    placeholder='Choose a subject',
                                                    clearable=False,
                                                    style={'background-color':
                                                           'rgba(223,223,218,0.7)',
                                                           'color': 'black',
                                                           'margin': '1% 1% 1% 1%'},
                                                    id='r-subject-dropdown',
                                                    className='dropdown'
                                                ),
                                                html.Div(id='r_subject_header2',
                                                         children=[html.H3('Subject information:'),
                                                                   html.Div(id='r-subject-information'),
                                                                   ],
                                                         ),
                                            ]),
                                   html.Div(id='r-subject-dropdown-container', className='right_container',
                                            children=[
                                                html.H3('Graph:'),
                                                dcc.Graph(id='r-subject-graph',
                                                          config=GRAPH_CONFIG,
                                                          ),
                                                html.Div(id='r-subject-container',
                                                         children=[
                                                             html.H3('Subject data:'),
                                                             html.Div(id='r-subject-table-container'),
                                                         ],
                                                         ),
                                            ]),
                               ])

geographical_information = html.Div(id='r_geo', className='container', children=[
    html.Div(id='r_geo_header', className='page_header', children=[
        html.H1('Rectores Magnifici')
    ]),
    html.Div(id='geo-map-container', className='left_container', children=[
        html.P('As of yet, there is no geographical information of the rectors.')
    ]),
]),

individual_information = html.Div(id='r_individual', className='container', children=[
    html.Div(id='r_student_header', className='page_header', children=[
        html.H1('Rectores Magnifici')
    ]),
    html.Div(id='r_inputs_left', className='middle_small_container ', children=[
        html.H3('Search settings:', className='inline'),
        html.P('Search for a name:', className='inline'),
        dcc.Input(
            id='r-search-name',
            type='text',
            placeholder='Search name',
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
            className='inline',
        ),
        dcc.RadioItems(
            inline=True,
            options=['Contains', 'Equals'],
            value='Contains',
            id='r-search-option',
            className='inline',
        ),
        html.Br(),
        html.P('Select term year range:', className='inline'),
        html.Br(),
        dcc.Input(
            id='term-min-input', className='inline',
            type='number',
            min=data.rector_years['year'].min(),
            max=data.rector_years['year'].max() - 1,
            value=data.rector_years['year'].min(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
        dcc.Input(
            id='term-max-input', className='inline',
            type='number',
            min=data.rector_years['year'].min() + 1,
            max=data.rector_years['year'].max(),
            value=data.rector_years['year'].max(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
        html.Br(),
        html.P('Include people with missing date values?', className='inline'),
        dcc.RadioItems(
            inline=True,
            options=['Yes', 'No'],
            value='Yes',
            id='r-include-missing-dates',
            className='inline',
        ),
        html.Br(),
        html.Br(),
        html.Button(
            'START SEARCH',
            id='r-search-individual',
            className='inline',
            style={'font-weight': 'bold', 'margin-left': '20%', 'height': '75px', 'width': '200px'},
        ),
        html.Br(),
        html.Br(),
    ]),
    html.Div(id='r-individual-information', className='middle_container', children=[
        html.H3(id='r-individual-search-results-header',),
        html.Div(id='r-individual-search-results', children=[
            html.Div(id='r-individual-search-results-number', className='inline', style={"font-weight": "bold"}),
            html.Div(id='r-individual-search-text', className='inline', style={'margin-left': '8px'})
        ]),
        html.Div(id='r-individual-table-container'),
        html.Div(id='r-individual-detailed-information', children=[
            html.Div(id='r-chosen-individual-information', children=[]),
            html.Div(id='r-chosen-individual-information-output'),
        ]),
        html.Div(id='r-individual-output'),
    ]),
]),
