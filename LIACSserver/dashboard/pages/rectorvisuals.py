# Creating dataframe
from dash import dcc, html
import data
from figures import rectorfigures

timeline = html.Div(id='r_timeline', className='container', children=[
    html.Div(id='r_timeline_header', className='page_header', children=[
        html.H1('Timeline')
    ]),
    html.Div(id='r-year-century-dropdown-container', className='left_container'),
    html.Div(id='r_inputs', className='right_container ', children=[
        html.H3('Graph settings:'),
        html.P('Select Subject:'),
        dcc.Dropdown(
            ['Rectors'], 'Rectors', placeholder='Choose a subject', clearable=False,
            id='r-year-century-subject-dropdown', className='dropdown'
        ),
        html.P('Select year range:'),
        html.Div(id='r-year-slider-container'),
        html.P('Select century range:'),
        dcc.RangeSlider(
            data.rector_years['century'].min(),
            data.rector_years['century'].max(),
            1,
            value=[data.rector_years['century'].min(), data.rector_years['century'].min()],
            marks={str(cent): str(cent) for cent in data.rector_years['century']},
            id='r-year-century-slider'
        ),
        html.P('Select graph type:'),
        dcc.Dropdown(
            ['Line graph', 'Scatter graph', 'Bar graph'], 'Scatter graph', placeholder='Choose a graph style',
            clearable=False, id='r-year-century-dropdown', className='dropdown'
        ),
    ]),
    html.Div(id='r-century-dropdown-container', className='left_container'),
    html.Div(id='r-timeline-information', className='right_container ', children=[
        html.H3('Information:'),
        html.Div(id='r-timeline-information'),
    ]),
]),

subject_information = html.Div(id='r_subject_info', className='container', children=[
    html.Div(id='r_subject_header', className='page_header', children=[
        html.H1('Subject information')
    ]),
    html.Div(id='r-subject-container', className='left_container', children=[
        html.Div(id='r-subject-dropdown-container'),
        html.H3('Subject information:'),
        html.Div(id='r-subject-table-container'),
    ]),
    html.Div(id='r-subject-information-container', className='right_container ', children=[
        html.H3('Subject information'),
        dcc.Dropdown(
            ['Rectors'], 'Rectors', placeholder='Choose a subject', clearable=False,
            style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1% 1% 1% 1%'},
            id='r-subject-dropdown', className='dropdown'
        ),
        html.Div(id='r-subject-information'),
    ]),
]),

geographical_information = html.Div(id='r_geo', className='container', children=[
    html.Div(id='r_geo_header', className='page_header', children=[
        html.H1('Geographical information')
    ]),
    html.Div(id='geo-map-container', className='left_container', children=[
        html.P('As of yet, there is no geographical information of the rectors.')
    ]),
]),

individual_information = html.Div(id='r_individual', className='container', children=[
    html.Div(id='r_student_header', className='page_header', children=[
        html.H1('Rector information')
    ]),
    html.Div(id='r_inputs_left', className='middle_small_container ', children=[
        html.H3('Search settings:', className='inline'),
        html.Button(
            'Search',
            id='r-search-individual',
            className='inline',
            style={'margin-left': '1%'}
        ),
        html.Br(),
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
        html.P('Select term year range', className='inline'),
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
            value='No',
            id='r-include-missing-dates',
            className='inline',
        ),
    ]),
    html.Div(id='r-individual-information', className='middle_container', children=[
        html.H3('Rector information:'),
        html.Div(id='r-individual-search-results', children=[
            html.Div(id='r-individual-search-results-number', className='inline'),
            html.Div(id='r-individual-search-text', className='inline', style={'margin-left': '1px'})
        ]),
        html.Div(id='r-individual-table-container'),
        html.Div(id='r-individual-detailed-information', children=[
            html.Div(id='r-chosen-individual-information', children=[]),
            html.Div(id='r-chosen-individual-information-output'),
        ]),
        html.Div(id='r-individual-output'),
    ]),
]),
