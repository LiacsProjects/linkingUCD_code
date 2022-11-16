# Creating dataframe
# Import modules
import dash
from dash import dcc, html
import data

# Parameters and constants
CENTURY_STEP     = 1
YEAR_STEP        = 5
MARK_SPACING     = 10
START_CENTURY    = 16
DEFAULT_SUBJECT = 'Appointment'
SUBJECT_DROPDOWN = ['Gender', 'Birth', 'Birth place', 'Birth country', 'Death', 'Death place', 
                    'Death country', 'Promotion', 'Promotion type', 'Promotion place', 'Appointment',
                    'Job', 'Subject area', 'Faculty', 'End of employment']
DEFAULT_GRAPH_SUBJECT = 'Appointment'
GRAPH_SUBJECT_DROPDOWN = ['Gender', 'Birth', 'Death', 'Promotion', 'Promotion type', 'Appointment',
                          'Job', 'Subject area', 'Faculty', 'End of employment']
GEOMAPS_OPTIONS  = ['Heat map', 'Line map', 'MP Heat map', 'MP Scatter map', 'Animated map']                  
DEFAULT_GRAPH = 'Bar graph'
GRAPH_DROPDOWN   = ['Line graph', 'Bar graph']



# Data year calculations
from figures import professorfigures
current_century = data.all_dates_df[(data.all_dates_df['century'] <= START_CENTURY)]
years = []
for y in current_century['year'][0::YEAR_STEP]:
        years.append(y)
years.append(current_century['year'].max())

# layout page 
timeline = html.Div(id='p_timeline', className='container',
                     children=[
                         html.Div(id='p_timeline_header', className='page_header',
                                  children=[html.H1('Timeline')]),
                         html.Div(id='p_inputs', className='left_container',
                                  children=[
                                      html.H3('Graph settings:'),
                                      html.P('Select Subject:'),
                                      dcc.Dropdown(SUBJECT_DROPDOWN, DEFAULT_SUBJECT,
                                                   placeholder='Choose a subject:', clearable=False,
                                                   id='p-year-century-subject-dropdown', className='dropdown'
                                                   ),
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
                                      html.Div(id='p-year-slider-container'),
                                      html.P('Select graph type:'),
                                      dcc.Dropdown(
                                          GRAPH_DROPDOWN, DEFAULT_GRAPH, placeholder='Choose a graph style',
                                          clearable=False, id='p-year-century-dropdown', className='dropdown'
                                          ),
                                      html.Div(id='p-year-century-graph'),
                                      ],
                                  ),
                         html.Div(id='p-year-century-dropdown-container', className='right_container',
                                  children=[
                                            html.H4('Graph:'),
                                            dcc.Graph(id='p-year-century-graph',)
                                           ],
                                  ),
                         html.Div(id='p-timeline-information-container', className='left_container ',
                                  children=[
                                            html.H3('Information:'),
                                            html.Div(id='p-timeline-information'),
                                           ]
                                  ),
                         html.Div(id='p-century-dropdown-container', className='right_container',
                                  children=[
                                            html.H4('Sorted bar graph:'),
                                            dcc.Graph(id='p-century-graph'),
                                           ]
                                  ),
                     ])

subject_information = html.Div(id='p_subject_info', className='container',
                               children=[
                                         html.Div(id='p_subject_header', className='page_header',
                                            children=[html.H1('Subject information')]),
                                         html.Div(id='p-subject-information-container', className='left_container',
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
                                                                   id='p-subject-dropdown',
                                                                   className='dropdown'
                                                                 ),
                                                      html.Div(id='p_subject_header2',
                                                                   children=[html.H3('Subject information:'),
                                                                             html.Div(id='p-subject-information'),
                                                                            ]
                                                         ),
                                                     ]),

                                         html.Div(id='p-subject-dropdown-container', className='right_container',
                                                  children=[
                                                            html.H3('Graph:'),
                                                            dcc.Graph(id='p-subject-graph'),
                                                            html.H3('Subject data:'),
                                                            html.Div(id='p-subject-table-container'),
                                                           ]),


                                     ])



geographical_information = html.Div(id='g_geo', className='container',
    children=[
              html.Div(id='g_geo_header', className='page_header',
                       children=[html.H1('Geographical information')]
                       ),
              html.Div(id='p-geo-map-container', className='right_container',
                       children=[
                                 html.H3('Geographical origin of professors'),
                                 html.Div(id='p-map-title'),
                                 html.Div(id='p-map-container'),
                                 html.P('Map with present day borders'),
                                 html.Div(id='p-animation-container'),
                                 html.P('Choose map:', className='inline'),
                                 dcc.RadioItems(
                                                inline=True,
                                                options=GEOMAPS_OPTIONS,
                                                value='Heat map',
                                                id='p-map-choice',
                                                className='inline',
                                                ),
        html.Br(),
        html.P('Select subject:', className='inline'),
        dcc.Dropdown(
            GRAPH_SUBJECT_DROPDOWN,
            DEFAULT_GRAPH_SUBJECT,
            placeholder='Choose a subject',
            clearable=False, id='p-geo-subject-dropdown', className='dropdown'
        ),
        html.Br(),
        html.P('Select year range:', className='inline'),
        html.P('Lowest year', className='inline'),
        dcc.Input(
            id='p-geo-min-input', className='inline',
            type='number',
            min=data.all_dates_df['year'].min(),
            max=data.all_dates_df['year'].max() - 1,
            value=data.all_dates_df['year'].min(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
        html.P('Highest year', className='inline'),
        dcc.Input(
            id='p-geo-max-input', className='inline',
            type='number',
            min=data.all_dates_df['year'].min() + 1,
            max=data.all_dates_df['year'].max(),
            value=data.all_dates_df['year'].max(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
    ]),
    html.Div(id='p-map-info', className='left_container', children=[
        html.H3('Country information'),
        html.Div(id='p-map-table-container'),
    ]),
]),

individual_information = html.Div(id='p_individual', className='container', children=[
    html.Div(id='p_Professor_header', className='page_header', children=[
        html.H1('Professor information')
    ]),
    html.Div(id='p_i_inputs_left', className='middle_small_container ', children=[
        html.H3('Search settings:', className='inline'),
        html.Button(
            'Search',
            id='p-search-individual',
            className='inline',
            style={'margin-left': '1%'}
        ),
        html.Br(),
        html.P('Search for a name:', className='inline'),
        dcc.Input(
            id='p-search-name',
            type='text',
            placeholder='Search name',
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
            className='inline',
        ),
        dcc.RadioItems(
            inline=True,
            options=['Contains', 'Equals'],
            value='Contains',
            id='p-search-option',
            className='inline',
        ),
        html.Br(),
        html.P('Select appointment year range', className='inline'),
        dcc.Input(
            id='appointment-min-input', className='inline',
            type='number',
            min=data.all_dates_df['year'].min(),
            max=data.all_dates_df['year'].max() - 1,
            value=data.all_dates_df['year'].min(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
        dcc.Input(
            id='appointment-max-input', className='inline',
            type='number',
            min=data.all_dates_df['year'].min() + 1,
            max=data.all_dates_df['year'].max(),
            value=data.all_dates_df['year'].max(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
        html.Br(),
        html.P('Select birthyear range:', className='inline'),
        dcc.Input(
            id='p-birthyear-min-input', className='inline',
            type='number',
            min=data.all_dates_df['year'].min(),
            max=data.all_dates_df['year'].max() - 1,
            value=data.all_dates_df['year'].min(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
        dcc.Input(
            id='p-birthyear-max-input', className='inline',
            type='number',
            min=data.all_dates_df['year'].min() + 1,
            max=data.all_dates_df['year'].max(),
            value=data.all_dates_df['year'].max(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
        html.Br(),
        html.P('Include people with missing date values?', className='inline'),
        dcc.RadioItems(
            inline=True,
            options=['Yes', 'No'],
            value='Yes',
            id='p-include-missing-dates',
            className='inline',
        ),
    ]),
    html.Div(id='p_i_inputs_right', className='middle_small_container ', children=[
        html.P('Select Gender:', className='inline'),
        dcc.Dropdown(professorfigures.get_unique_values('Gender'), placeholder='Choose a gender', clearable=False,
                     multi=True, id='p-individual-gender-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select birth place:', className='inline'),
        dcc.Dropdown(professorfigures.get_unique_values('Birth place'), placeholder='Choose a birth place',
                     clearable=False,
                     multi=True, id='p-individual-birthplace-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select birth country:', className='inline'),
        dcc.Dropdown(professorfigures.get_unique_values('Birth country'), placeholder='Choose a birth country',
                     clearable=False,
                     multi=True, id='p-individual-birthcountry-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select death place:', className='inline'),
        dcc.Dropdown(professorfigures.get_unique_values('Death place'), placeholder='Choose a death place',
                     clearable=False,
                     multi=True, id='p-individual-deathplace-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select death country:', className='inline'),
        dcc.Dropdown(professorfigures.get_unique_values('Death country'), placeholder='Choose a death country',
                     clearable=False,
                     multi=True, id='p-individual-deathcountry-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select promotion:', className='inline'),
        dcc.Dropdown(professorfigures.get_unique_values('Promotion'), placeholder='Choose a promotion', clearable=False,
                     multi=True, id='p-individual-promotion-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select promotion place:', className='inline'),
        dcc.Dropdown(professorfigures.get_unique_values('Promotion place'), placeholder='Choose a promotion place',
                     clearable=False,
                     multi=True, id='p-individual-promotionplace-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select thesis:', className='inline'),
        dcc.Dropdown(professorfigures.get_unique_values('Thesis'), placeholder='Choose a thesis',
                     clearable=False,
                     multi=True, id='p-individual-thesis-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select job:', className='inline'),
        dcc.Dropdown(professorfigures.get_unique_values('Job'), placeholder='Choose a job',
                     clearable=False,
                     multi=True, id='p-individual-job-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select subject area:', className='inline'),
        dcc.Dropdown(professorfigures.get_unique_values('Subject area'), placeholder='Choose a subject area',
                     clearable=False,
                     multi=True, id='p-individual-subjectarea-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select faculty:', className='inline'),
        dcc.Dropdown(professorfigures.get_unique_values('Faculty'), placeholder='Choose a faculty',
                     clearable=False,
                     multi=True, id='p-individual-faculty-dropdown', className='dropdown'),
    ]),
    html.Div(id='p-individual-information', className='middle_container', children=[
        html.H3('Professor information:'),
        html.Div(id='p-individual-search-results', children=[
            html.Div(id='p-individual-search-results-number', className='inline'),
            html.Div(id='p-individual-search-text', className='inline', style={'margin-left': '1px'})
        ]),
        html.Div(id='p-individual-table-container'),
        html.Div(id='p-individual-detailed-information', children=[
            html.Div(id='p-chosen-individual-information', children=[]),
            html.Div(id='p-chosen-individual-information-output'),
        ]),
        html.Div(id='p-individual-output'),
    ]),
]),
