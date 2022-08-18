# Creating dataframe
import dash
from dash import dcc, html
import data
from figures import studentfigures

timeline = html.Div(id='p_timeline', className='container', children=[
    html.Div(id='p_timeline_header', className='page_header', children=[
        html.H1('Timeline')
    ]),
    html.Div(id='p-year-century-dropdown-container', className='left_container'),
    html.Div(id='p_inputs', className='right_container ', children=[
        html.H3('Graph settings:'),
        html.P('Select Subject:'),
        dcc.Dropdown(
            ['Number of enrollments', 'Origin countries', 'Origin cities', 'Enrollment ages',
             'Enrollment faculties', 'Royal status', 'Student jobs', 'Student religion'],
            'Number of enrollments', placeholder='Choose a subject', clearable=False,
            id='p-year-century-subject-dropdown', className='dropdown'
        ),
        html.P('Select year range:'),
        html.Div(id='p-year-slider-container'),
        html.P('Select century range:'),
        dcc.RangeSlider(
            data.year_df['century'].min(),
            data.year_df['century'].max(),
            1,
            value=[data.year_df['century'].min(), data.year_df['century'].min()],
            marks={str(cent): str(cent) for cent in data.year_df['century']},
            id='p-year-century-slider'
        ),
        html.P('Select graph type:'),
        dcc.Dropdown(
            ['Line graph', 'Scatter graph', 'Bar graph'], 'Scatter graph', placeholder='Choose a graph style',
            clearable=False, id='p-year-century-dropdown', className='dropdown'
        ),
        html.P('Select age range:'),
        dcc.RangeSlider(
            data.age_df['age'].min(),
            data.age_df['age'].max(),
            10,
            value=[data.age_df['age'].min(), data.age_df['age'].max()],
            id='p-subject-slider'
        ),
    ]),
    html.Div(id='p-century-dropdown-container', className='left_container'),
    html.Div(id='p-timeline-information', className='right_container ', children=[
        html.H3('Information:'),
        html.Div(id='p-timeline-information'),
    ]),
]),

subject_information = html.Div(id='s_subject_info', className='container', children=[
    html.Div(id='s_subject_header', className='page_header', children=[
        html.H1('Subject information')
    ]),
    html.Div(id='subject-container', className='left_container', children=[
        html.Div(id='subject-dropdown-container'),
        html.H3('Subject information:'),
        html.Div(id='subject-table-container'),
    ]),
    html.Div(id='subject-information-container', className='right_container ', children=[
        html.H3('Subject information'),
        dcc.Dropdown(
            ['Number of enrollments', 'Origin countries', 'Origin cities', 'Origin regions',
             'Enrollment ages', 'Enrollment faculties', 'Royal status', 'Student jobs', 'Student religion'],
            'Number of enrollments', placeholder='Choose a subject', clearable=False,
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1% 1% 1% 1%'},
            id='subject-dropdown', className='dropdown'
        ),
        html.Div(id='subject-information'),
    ]),
]),

geographical_information = html.Div(id='s_geo', className='container', children=[
    html.Div(id='s_geo_header', className='page_header', children=[
        html.H1('Geographical information')
    ]),
    html.Div(id='geo-map-container', className='left_container', children=[
        html.H3('Student enrollments per country'),
        html.Div(id='map-title'),
        html.Div(id='map-container'),
        html.Div(id='animation-container'),
        html.P('Choose map:', className='inline'),
        dcc.RadioItems(
            inline=True,
            options=['Heat map', 'Line map', 'MP Heat map', 'MP Scatter map', 'Animated map'],
            value='Heat map',
            id='map-choice',
            className='inline',
        ),
        html.Br(),
        html.P('Select subject:', className='inline'),
        dcc.Dropdown([
            'Number of enrollments', 'Origin cities', 'Enrollment ages', 'Enrollment faculties', 'Royal status',
            'Student jobs', 'Student religion'], 'Number of enrollments', placeholder='Choose a subject',
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
    html.Div(id='map-info', className='right_container', children=[
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
        html.P('Select enrollment year range', className='inline'),
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
            value='No',
            id='include-missing-dates',
            className='inline',
        ),
        html.Br(),
        html.P('Select enrollment age:'),
        dcc.RangeSlider(
            int(data.individual_df['Enrollment age'].min()),
            int(data.individual_df['Enrollment age'].max()),
            10,
            value=[int(data.individual_df['Enrollment age'].min()), int(data.individual_df['Enrollment age'].max())],
            id='individual-age-slider'
        ),
    ]),
    html.Div(id='i_inputs_right', className='middle_small_container ', children=[
        html.P('Select cities:', className='inline'),
        dcc.Dropdown(studentfigures.get_unique_values('City'), placeholder='Choose a city', clearable=False,
                     multi=True, id='individual-city-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select countries:', className='inline'),
        dcc.Dropdown(data.individual_df['Country'].unique(), placeholder='Choose a country', clearable=False,
                     multi=True, id='individual-country-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select region:', className='inline'),
        dcc.Dropdown(data.individual_df['Region'].unique(), placeholder='Choose a region', clearable=False,
                     multi=True, id='individual-region-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select faculty:', className='inline'),
        dcc.Dropdown(data.individual_df['Faculty'].unique(), placeholder='Choose a faculty', clearable=False,
                     multi=True, id='individual-faculty-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select royal title:', className='inline'),
        dcc.Dropdown(studentfigures.remove_nan('Royal title'), placeholder='Choose a royal title', clearable=False,
                     multi=True, id='individual-royal-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select job:', className='inline'),
        dcc.Dropdown(studentfigures.remove_nan('Job'), placeholder='Choose a job', clearable=False,
                     multi=True, id='individual-job-dropdown', className='dropdown'),
        html.Br(),
        html.P('Select religion:', className='inline'),
        dcc.Dropdown(studentfigures.remove_nan('Religion'), placeholder='Choose a religion', clearable=False,
                     multi=True, id='individual-religion-dropdown', className='dropdown'),
    ]),
    html.Div(id='individual-information', className='middle_container', children=[
        html.H3('Student information:'),
        html.Div(id='individual-search-results', children=[
            html.Div(id='individual-search-results-number', className='inline'),
            html.Div(id='individual-search-text', className='inline', style={'margin-left': '1px'})
        ]),
        html.Div(id='individual-table-container'),
        html.Div(id='individual-detailed-information', children=[
            html.Div(id='chosen-individual-information', children=[]),
            html.Div(id='chosen-individual-information-output'),
        ]),
        html.Div(id='individual-output'),
    ]),
]),
