# Creating dataframe
# Import modules
import dash
from dash import dcc, html
import data

# Parameters and constants
CENTURY_STEP     = 1
YEAR_STEP        = 5
AGE_STEP         = 10
MARK_SPACING     = 10
START_CENTURY    = 16
DEFAULT_SUBJECT = 'Number of enrollments'
SUBJECT_DROPDOWN = ['Number of enrollments', 'Origin countries', 'Origin cities', 'Enrollment ages',
                   'Enrollment faculties', 'Royal status', 'Student jobs', 'Student religion']
DEFAULT_GRAPH_SUBJECT = 'Number of enrollments'
GRAPH_SUBJECT_DROPDOWN = ['Number of enrollments', 'Origin cities', 'Enrollment ages', 'Enrollment faculties', 
                          'Royal status', 'Student jobs', 'Student religion']
GEOMAPS_OPTIONS  = ['Heat map', 'Line map', 'MP Heat map', 'MP Scatter map', 'Animated map']
DEFAULT_GRAPH = 'Bar graph'
GRAPH_DROPDOWN   = ['Line graph', 'Bar graph']

# Data year calculaionss
from figures import studentfigures
current_century = data.all_dates_df[(data.all_dates_df['century'] <= START_CENTURY)]
years = []
for y in current_century['year'][0::YEAR_STEP]:
        years.append(y)
years.append(current_century['year'].max() )

# layout page 
timeline = html.Div(id='s_timeline', className='container',
                    children=[
                               html.Div(id='s_timeline_header', className='page_header',
                                        children=[html.H1('Timeline')]),
                               html.Div(id='s_inputs', className='left_container ',
                                  children=[
                                            html.H3('Graph settings:'),
                                            html.P('Select Subject:'),
                                            dcc.Dropdown(
                                                         SUBJECT_DROPDOWN,
                                                         DEFAULT_SUBJECT,
                                                         placeholder='Choose a subject',
                                                         clearable=False,
                                                         id='year-century-subject-dropdown',
                                                         className='dropdown'
                                                        ),
                                            html.P('Select century range:'),
                                            dcc.RangeSlider(
                                                            data.year_df['century'].min(),
                                                            data.year_df['century'].max(),
                                                            CENTURY_STEP,
                                                            value=[data.year_df['century'].min(),
                                                                   data.all_dates_df['century'].min()],
                                                            marks={str(cent):
                                                                    str(cent) for cent in data.all_dates_df['century']},
                                                            id='year-century-slider'
                                                            ),
                                            html.P('Select year range:'),
                                            dcc.RangeSlider(
                                                            current_century['year'].min(),
                                                            current_century['year'].max(),
                                                            YEAR_STEP,
                                                            id='year-slider',
                                                           ),
                                            html.Div(id='year-slider-container'),
                                            html.P('Select graph type:'),
                                            dcc.Dropdown(
                                                          GRAPH_DROPDOWN, DEFAULT_GRAPH,
                                                          placeholder='Choose a graph style',
                                                          clearable=False,
                                                          id='year-century-dropdown', className='dropdown'
                                                         ),
                                           html.P('Select age range:'),
                                           dcc.RangeSlider(
                                                           data.age_df['age'].min(),
                                                           data.age_df['age'].max(),
                                                           AGE_STEP,
                                                           value=[data.age_df['age'].min(), data.age_df['age'].max()],
                                                           id='subject-slider'
                                                          ),
                                    ],
                            ),
           html.Div(id='year-century-dropdown-container', className='right_container',
                                 children= [
                                           html.H4('Graph:'),
                                           dcc.Graph(id='year-century-graph',),
                                           ],
                                 ),
           html.Div(id='timeline-information', className='left_container ',
                    children=[
                              html.H3('Information:'),
                              html.Div(id='timeline-information'),
                             ]
                    ),
           html.Div(id='century-dropdown-container', className='right_container',
                    children=[
                              html.H4('Sorted bar graph'),
                              dcc.Graph(id='century-graph')
                             ]
                    ),
              ] )

subject_information = html.Div(id='s_subject_info', className='container',
                               children=[
                                         html.Div(id='s_subject_header', className='page_header',
                                                  children=[
                                                            html.H1('Subject information')
                                                           ]
                                                  ),
                                          html.Div(id='subject-information-container', className='left_container ',
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
                                                                          id='subject-dropdown',
                                                                          className='dropdown'
                                                                         ),
                                                             html.Div(id='subject_header2',
                                                                children=[html.H3('Subject information:'),
                                                                          html.Div(id='subject-information')
                                                                          ]
                                                                ),
                                                            ]),

                                   html.Div(id='subject-dropdown-container', className='right_container',
                                            children=[
                                                html.H3('Graph:'),
                                                dcc.Graph(id='subject-graph'),
                                                html.H3('Subject data:'),
                                                html.Div(id='subject-table-container'),
                                            ]
                                            ),
                                       ]),

geographical_information = html.Div(id='s_geo', className='container', children=[
    html.Div(id='s_geo_header', className='page_header', children=[
        html.H1('Geographical information')
    ]),
    html.Div(id='geo-map-container', className='right_container', children=[
        html.H3('Geographical origin of students'),
        html.Div(id='map-title'),
        html.Div(id='map-container'),
        html.Div(id='animation-container'),
        html.P('Map with present day borders'),
        html.P('Choose map:', className='inline'),
        dcc.RadioItems(
            inline=True,
            options=GEOMAPS_OPTIONS,
            value='Heat map',
            id='map-choice',
            className='inline',
        ),
        html.Br(),
        # html.A('Go to globe', href='assets/mapboxLeiden.html', target='_blank', rel='noreferrer noopener'),
        # html.Br(),
        html.P('Select subject:', className='inline'),
        dcc.Dropdown(
            GRAPH_SUBJECT_DROPDOWN,
            'Number of enrollments', 
            placeholder='Choose a subject',
            clearable=False, id='geo-subject-dropdown', className='dropdown'
        ),
        html.Br(),
        html.P('Select year range:', className='inline'),
        html.P('Lowest year', className='inline'),
        dcc.Input(
            id='geo-min-input', className='inline',
            type='number',
            min=data.year_df['year'].min(),
            max=data.year_df['year'].max() - 1,
            value=data.year_df['year'].min(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
        html.P('Highest year', className='inline'),
        dcc.Input(
            id='geo-max-input', className='inline',
            type='number',
            min=data.year_df['year'].min() + 1,
            max=data.year_df['year'].max(),
            value=data.year_df['year'].max(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
    ]),
    html.Div(id='map-info', className='left_container', children=[
        html.H3('Country information'),
        html.Div(id='map-table-container'),
    ]),
]),

individual_information = html.Div(id='s_individual', className='container', children=[
    html.Div(id='s_student_header', className='page_header', children=[
        html.H1('Student information')
    ]),
    html.Div(id='i_inputs_left', className='middle_small_container ', children=[
        html.H3('Search settings:', className='inline'),
        html.Button(
            'Search',
            id='search-individual',
            className='inline',
            style={'margin-left': '1%'}
        ),
        html.Br(),
        html.P('Search for a name:', className='inline'),
        dcc.Input(
            id='search-name',
            type='text',
            placeholder='Search name',
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
            className='inline',
        ),
        dcc.RadioItems(
            inline=True,
            options=['Contains', 'Equals'],
            value='Contains',
            id='search-option',
            className='inline',
        ),
        html.Br(),
        html.P('Select enrollment year range:', className='inline'),
        html.Br(),
        dcc.Input(
            id='enrollment-min-input', className='inline',
            type='number',
            min=data.year_df['year'].min(),
            max=data.year_df['year'].max() - 1,
            value=data.year_df['year'].min(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
        dcc.Input(
            id='enrollment-max-input', className='inline',
            type='number',
            min=data.year_df['year'].min() + 1,
            max=data.year_df['year'].max(),
            value=data.year_df['year'].max(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
        html.Br(),
        html.P('Select birthyear range:', className='inline'),
        html.Br(),
        dcc.Input(
            id='birthyear-min-input', className='inline',
            type='number',
            min=data.year_df['year'].min(),
            max=data.year_df['year'].max() - 1,
            value=data.year_df['year'].min(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
        dcc.Input(
            id='birthyear-max-input', className='inline',
            type='number',
            min=data.year_df['year'].min() + 1,
            max=data.year_df['year'].max(),
            value=data.year_df['year'].max(),
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
        ),
        html.Br(),
        html.P('Include people with missing date values?', className='inline'),
        dcc.RadioItems(
            inline=True,
            options=['Yes', 'No'],
            value='Yes',
            id='include-missing-dates',
            className='inline',
        ),
        html.Br(),
        html.P('Select enrollment age:'),
        dcc.RangeSlider(
            int(data.individual_student_df['Enrollment age'].min()),
            int(data.individual_student_df['Enrollment age'].max()),
            10,
            value=[int(data.individual_student_df['Enrollment age'].min()), int(data.individual_student_df['Enrollment age'].max())],
            id='individual-age-slider'
        ),
    ]),
    html.Div(id='i_inputs_right', className='middle_small_container ', children=[
        html.Table([
            html.Tr([
                 html.Td(html.P('Select cities:', className='inline'), ),
                 html.Td(dcc.Dropdown(studentfigures.get_unique_values('City'), placeholder='Choose a city',
                                      clearable=False, multi=True, id='individual-city-dropdown',
                                      className='dropdown', style={"width": "400px"}), ),
                    ]),
            html.Tr([
                 html.Td(html.P('Select countries:', className='inline'), ),
                 html.Td(dcc.Dropdown(data.individual_student_df['Country'].unique(), placeholder='Choose a country',
                                       clearable=False, multi=True, id='individual-country-dropdown',
                                       className='dropdown', style={"width": "400px"}), ),
                    ]),
            html.Tr([
                 html.Td(html.P('Select region:', className='inline'), ),
                 html.Td(dcc.Dropdown(data.individual_student_df['Region'].unique(), placeholder='Choose a region',
                                      clearable=False, multi=True, id='individual-region-dropdown',
                                      className='dropdown', style={"width": "400px"}), ),
                    ]),
            html.Tr([
                html.Td(
                html.P('Select faculty:', className='inline'), ),
                html.Td(dcc.Dropdown(data.individual_student_df['Faculty'].unique(), placeholder='Choose a faculty',
                                     clearable=False, multi=True, id='individual-faculty-dropdown',
                                     className='dropdown', style={"width": "400px"}), ),
                    ]),
            html.Tr([
                html.Td(html.P('Select royal title:', className='inline'), ),
                html.Td(dcc.Dropdown(studentfigures.remove_nan('Royal title'), placeholder='Choose a royal title',
                                     clearable=False, multi=True, id='individual-royal-dropdown', className='dropdown',
                                     style={"width": "400px"}), ),
                    ]),
            html.Tr([
                html.Td(html.P('Select job:', className='inline'), ),
                html.Td(dcc.Dropdown(studentfigures.remove_nan('Job'), placeholder='Choose a job', clearable=False,
                                     multi=True, id='individual-job-dropdown', className='dropdown',
                                     style={"width": "400px"}), ),
                    ]),
            html.Tr([
                html.Td(html.P('Select religion:', className='inline'), ),
                html.Td(dcc.Dropdown(studentfigures.remove_nan('Religion'), placeholder='Choose a religion',
                                     clearable=False, multi=True, id='individual-religion-dropdown',
                                     className='dropdown', style={"width": "400px"}), ),
                    ]),
        ])
    ]),
    html.Div(id='individual-information', className='middle_container', children=[
        html.H3('Student search data:'),
        html.Div(id='individual-search-results', children=[
            html.Div(id='individual-search-results-number', className='inline', style={"font-weight":"bold"}),
            html.Div(id='individual-search-text', className='inline', style={'margin-left': '8px'})
        ]),
        html.Div(id='individual-table-container'),
        html.Div(id='individual-detailed-information', children=[
            html.Div(id='chosen-individual-information', children=[]),
            html.Div(id='chosen-individual-information-output'),
        ]),
        html.Div(id='individual-output'),
    ]),
]),
