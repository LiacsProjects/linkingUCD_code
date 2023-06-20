############################################################################################## LOCAL
# added for local server
# extra regel om environmental variable te bepalen
#import Add_environment_variable

########################################################################################### end local
# import modules
from dash import Dash, dcc, html, Input, Output, ctx, dash_table, State, ALL
import pandas as pd

# import data, page lay-outs and functions
import data
from figures import studentfigures
from pages import professorvisuals, rectorvisuals, studentvisuals
from figures import professorfigures, studentfigures, rectorfigures

# Parameters and constants
YEAR_STEP = 5
MARK_SPACING = 10
################################################################################################ LOCAL
# Configurate dash application voor DASH
app = Dash(__name__, suppress_callback_exceptions=True,
           routes_pathname_prefix='/',
           requests_pathname_prefix='/dashboard/'
           )
           
################################################################################################ SERVER
# Configurate dash application voor server
server = app.server

########################################################################################################### TODO

# TODO: implement store functions to allow users to save their changes made to the dashboard TODO: connect database to dashboard
# TODO: create joined page for all persons TODO: link city/country coordinates to city/country dataframes, preferably through function that reads coordinates from a file: countries.geojson and cities1-2-3.csv

########################################################################################################### START

app.layout = html.Div([
    html.H1('Linking University and City in Leiden, 1575-2020', id='page_title'),
    dcc.Tabs(id='tab_bar', value='tab-0', className='header_tab_bar', children=[
        dcc.Tab(label='Home', value='tab-0', className='child_tab', selected_className='child_tab_selected'),
        dcc.Tab(label='Professors', value='tab-1', className='child_tab', selected_className='child_tab_selected'),
        dcc.Tab(label='Students', value='tab-2', className='child_tab', selected_className='child_tab_selected'),
        dcc.Tab(label='Rectores Magnifici', value='tab-3', className='child_tab',
                selected_className='child_tab_selected'),
        dcc.Tab(label='Colofon', value='tab-4', className='child_tab',
                selected_className='child_tab_selected'),
        ]),
    html.Div(id='page_content'),
])

home_content = html.Div(id='h_content', className='parent_content', children=[
    html.Div(id='h_info', className='container', children=[
        html.H2('Welcome'),
        html.P('Leiden University was founded in 1575. '
               'Since then, many thousands of students and staff have attended the university. '
               'Who were they? Where did they come from?  '
               'How did the academic population change over time? '
               'This website allows you to explore and visualise the answers to these questions. '
               'You can search for information on students and on academic staff.'),
        html.H2('The project'),
        html.P('This website is part of, and presents the first results of the project '
               'Linking University and City in Leiden 1575-2020. '
               'The aim of the project is to examine the interaction between the university and the city. '
               'The impact of the presence of the university on the city has been described '
               'from different perspectives, but we know little about the interaction between '
               'the changing populations in town and gown. '
               'The presence of an academic population affected the urban demography, '
               'social-economic structures and culture. '
               'The urban dynamics related to migration and socio-economic development '
               'may -vice versa- have had impact on the university. The question is how.'  
               'This project will examine the interaction between university and city through data science methods.'),
        html.P('This project is work-in-progress. Data on the website will be regularly updated '
               'and the functionalities will be extended'),
        html.Div(className='center_object', children=[
            html.Embed(src='assets/LEI001013879.jpg', width='40%', height='40%',
                       title=('Academiegebouw, Rapenburg 73. '
                              'Academie met op de voorgrond ijsvermaak op het Rapenburg.' 
                              'Foto van een tekening in het album Amicorum van Johannes van Amstel '
                              'van Mijnden, 1601, in Koninklijke Bibliotheek te Den Haag.')),
            html.P('Erfgoed Leiden en Omstreken', style={'font-size': 'small'})
        ]),
    ]),
])

profs_content = html.Div(id='p_content', className='parent_content', children=[
    html.H2('Information'),
    html.P('This page shows the information about professors previously working at the university of Leiden.'
           ' Choose one of the following options to see more information.'),
    dcc.Tabs(id='p_tab_bar', value='p_tab-1', className='header_tab_bar', children=[
        dcc.Tab(label='Timeline', value='p_tab-1', className='child_tab', selected_className='child_tab_selected'),
        dcc.Tab(label='Subject information', value='p_tab-2', className='child_tab',
                selected_className='child_tab_selected'),
        dcc.Tab(label='Geographical information', value='p_tab-3', className='child_tab',
                selected_className='child_tab_selected'),
        dcc.Tab(label='Individual information', value='p_tab-4', className='child_tab',
                selected_className='child_tab_selected'),
    ]),
    html.Div(id='professor_page_content'),
])

students_content = html.Div(id='s_content', className='parent_content', children=[
    html.Div(id='s_info', className='container', children=[
        html.H2('Information'),
        html.P('This page shows the information about student enrollments from the period 1575 to 1812. Choose one of '
               'the following options to see details about the enrollments of students at the university of Leiden.'),
        dcc.Tabs(id='s_tab_bar', value='s_tab-1', className='header_tab_bar', children=[
            dcc.Tab(label='Timeline', value='s_tab-1', className='child_tab', selected_className='child_tab_selected'),
            dcc.Tab(label='Subject information', value='s_tab-2', className='child_tab',
                    selected_className='child_tab_selected'),
            dcc.Tab(label='Geographical information', value='s_tab-3', className='child_tab',
                    selected_className='child_tab_selected'),
            dcc.Tab(label='Individual information', value='s_tab-4', className='child_tab',
                    selected_className='child_tab_selected'),
        ]),
    ]),
    html.Div(id='student_page_content'),
])

rector_content = html.Div(id='r_content', className='parent_content', children=[
    html.H2('Information'),
    html.P('This page shows the information about all the rectores magnifici the university of Leiden has had.'
           ' Choose one of the following options to see more information.'),
    dcc.Tabs(id='r_tab_bar', value='r_tab-1', className='header_tab_bar', children=[
        dcc.Tab(label='Timeline', value='r_tab-1', className='child_tab', selected_className='child_tab_selected'),
        dcc.Tab(label='Subject information', value='r_tab-2', className='child_tab',
                selected_className='child_tab_selected'),
        dcc.Tab(label='Geographical information', value='r_tab-3', className='child_tab',
                selected_className='child_tab_selected'),
        dcc.Tab(label='Individual information', value='r_tab-4', className='child_tab',
                selected_className='child_tab_selected'),
    ]),
    html.Div(id='rector_page_content'),
])

sources_content = html.Div(id='src_content', className='parent_content', children=[
    html.Div(id='src_info', className='container', children=[
        html.H2('ABOUT THIS SITE'),
        html.P('This website is part of the project Linking City, University and Diversity'
               'This website is work in progress. The dataset is not yet complete, '
               'information on the website will be updated periodically.'),
        html.H2('Projectteam', style={"text-align":"left"}),
        html.P('Prof. dr Wessel Kraaij, Prof. dr Ariadne Schmidt (supervisors), '
               'Prof. dr Joost Visser, Ir. Richard van Dijk (projectlead software, LIACS software lab), '
               'Michael de Koning, Ben van Yperen (student assistants).'),
        html.H2('Datasources', style={"text-align":"left"}),
        html.P('The following sources are being used for this dashboard:'),
        html.Li('Dataset Martine Zoeteman, Student Population Leiden University 1575-1812 (2011), based upon Album Studiosorum.'
               'For an extensive explanation of the sources see:'  
               'Martine Zoeteman-van Pelt, De studentenpopulatie van de Leidse universiteit, 1575-1812; :'
               ' "Een volk op zyn Siams gekleet eenige mylen van Den Haag woonende" (Leiden 2011).'),
        html.Li(children=[
            html.A("https://hoogleraren.universiteitleiden.nl/ ",
                   href="https://hoogleraren.universiteitleiden.nl/"),
           'More information about this source can be found at ',
            html.A("https://hoogleraren.universiteitleiden.nl/toelichting",
                    href="https://hoogleraren.universiteitleiden.nl/toelichting"),
                          ]),
        html.Li('Additional information on rectors magnifici is retrieved from Wikipedia'),
        html.H2('Student projects', style={"text-align":"left"}),
        html.Li('Liam van Dreumel, ‘Visualisation tools to support historical research on a linked dataset about Leiden University’ BA thesis Computer Science, Leiden University.'),
        html.Li('Rick Schreuder, ‘Design of a database supporting the exploration of historical documents and linked register data’ BA thesis Computer Science, Leiden University.'),
        html.Li('Michael de Koning ‘Extraction, transformation, linking and loading of cultural heritage data’ BA thesis Computer Science, Leiden University.'),
        html.H2('Credits', style={"text-align":"left"}),
        html.P('We like to thank Martine Zoeteman, Saskia van Bergen, Stelios Paraschiakos, Antonis Somorakis, Wout Lamers, '
               'Leida van Hees and Carel Stolker for their contributions to this project. '),
        html.H2('Contact', style={"text-align":"left"}),
        html.P('Ariadne Schmidt,  Wessel Kraaij'),
    ]),
])


# Index callbacks
@app.callback(
    Output('page_content', 'children'),
    Input('tab_bar', 'value')
)
def render_content(tab):
    if tab == 'tab-0':
        return home_content
    if tab == 'tab-1':
        return profs_content
    if tab == 'tab-2':
        return students_content
    if tab == 'tab-3':
        return rector_content
    if tab == 'tab-4':
        return sources_content
    else:
        return 404


# Professor tabs
@app.callback(
    Output('professor_page_content', 'children'),
    Input('p_tab_bar', 'value')
)
def render_content(tab):
    if tab == 'p_tab-1':
        return professorvisuals.timeline
    if tab == 'p_tab-2':
        return professorvisuals.subject_information
    if tab == 'p_tab-3':
        return professorvisuals.geographical_information
    if tab == 'p_tab-4':
        return professorvisuals.individual_information
    else:
        return 404


# Student tabs
@app.callback(
    Output('student_page_content', 'children'),
    Input('s_tab_bar', 'value')
)
def render_content(tab):
    if tab == 's_tab-1':
        return studentvisuals.timeline
    if tab == 's_tab-2':
        return studentvisuals.subject_information
    if tab == 's_tab-3':
        return studentvisuals.geographical_information
    if tab == 's_tab-4':
        return studentvisuals.individual_information
    else:
        return 404


# Rector Magnificus tabs
@app.callback(
    Output('rector_page_content', 'children'),
    Input('r_tab_bar', 'value')
)
def render_content(tab):
    if tab == 'r_tab-1':
        return rectorvisuals.timeline
    if tab == 'r_tab-2':
        return rectorvisuals.subject_information
    if tab == 'r_tab-3':
        return rectorvisuals.geographical_information
    if tab == 'r_tab-4':
        return rectorvisuals.individual_information
    else:
        return 404

###################################################################### 
# Professor callbacks
###################################################################### 


# Year slider
@app.callback(
    Output('p-year-slider', 'min'),
    Output('p-year-slider', 'max'),
    Output('p-year-slider', 'value'),
    Output('p-year-slider', 'marks'),
    Input('p-year-century-slider', 'value')
)
def update_year_slider(century):
    current_century = data.all_dates_df[(data.all_dates_df['century'] <= century[-1])]
    years = []
    for y in current_century['year'][0::YEAR_STEP]:
        years.append(y)
    years.append(current_century['year'].max())
    min = current_century['year'].min()
    max = current_century['year'].max()
    value = [current_century['year'].min(), current_century['year'].max()]
    marks: dict = {str(year): str(year) for year in 
                   range(current_century['year'].min(), current_century['year'].max(),
                   int((current_century['year'].max() - current_century['year'].min()) / MARK_SPACING))}
    return min, max, value, marks


# year-century graph
@app.callback(
    Output('p-year-century-dropdown-container', 'children'),
    Input('p-year-century-subject-dropdown', 'value'),
    Input('p-year-century-slider', 'value'),
    Input('p-year-slider', 'value'),
    Input('p-year-century-dropdown', 'value'),
    running=[
             (Output('p-year-century-subject-dropdown', 'disabled'), True, False),
            ],
)
def update_year_century_output(selected_subject, selected_century, selected_year, selected_dropdown):
    return dcc.Graph(figure=professorfigures.create_year_cent_figure(selected_subject, selected_century, selected_year,
                                                                     selected_dropdown), 
                     id='p-year-century-graph')


# century-graph
@app.callback(
    Output('p-century-dropdown-container', 'children'),
    Input('p-year-century-subject-dropdown', 'value'),
    Input('p-year-century-slider', 'value'),
)
def update_century_output(selected_subject, selected_century):
    return dcc.Graph(figure=professorfigures.create_cent_figure(selected_subject, selected_century), id='century-graph')


# Timeline information
@app.callback(
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
                html.Td('Highest Year'),
                html.Td(df.loc[df['count'] == df['count'].max(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Least appointments'),
                html.Td(df['count'].min()),
            ]),
            html.Tr(children=[
                html.Td('Lowest Year'),
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
                html.Td('Highest Year'),
                html.Td(df.loc[df['count'] == df['count'].max(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Least appointments'),
                html.Td(df['count'].min()),
            ]),
            html.Tr(children=[
                html.Td('Lowest Year'),
                html.Td(df.loc[df['count'].min(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Average appointments'),
                html.Td(round(df['count'].mean(), 0)),
            ]),
        ]),


# Subject information callbacks
# Subject-graph
@app.callback(
    Output('p-subject-dropdown-container', 'children'),
    Input('p-subject-dropdown', 'value'),
    running=[
        (Output('p-subject-dropdown', 'disabled'), True, False),
    ],
)
def update_subject_output(selected_subject):
    return dcc.Graph(figure=professorfigures.create_subject_info_graph(selected_subject), id='p-subject-graph')


# Subject table
@app.callback(
    Output('p-subject-table-container', 'children'),
    Input('p-subject-dropdown', 'value'),
    )
def update_timeline_table(selected_subject):
    df, subject, name = professorfigures.get_variables(selected_subject)
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


# Subject information
@app.callback(
    Output('p-subject-information', 'children'),
    Input('p-subject-dropdown', 'value'),
    Input('p-subject-graph', 'hoverData'),
    )
def update_timeline_information(selected_subject, hover_data):
    if hover_data is not None:
        text = hover_data['points'][0]['hovertext']
    else:
        text = None
    df, subject, name = professorfigures.get_variables(selected_subject)
    total = df['count'].sum()
    fraction = df.loc[df[subject] == text, 'count'].sum()
    percentage = round(fraction / total * 100, 2)
    if subject == 'year':
        return html.Div(id='p-subject-hover-info', children=[
            html.Table(id='p-subject-table', children=[
                html.Tr(children=[
                    html.Td('Subject'),
                    html.Td(selected_subject),
                ]),
                html.Tr(children=[
                    html.Td(str(name) + ' amount'),
                    html.Td(df[subject].nunique()),
                ]),
                html.Tr(children=[
                    html.Td('Total appointments'),
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
                    html.Td('Appointments'),
                    html.Td(fraction),
                ]),
                html.Tr(children=[
                    html.Td('Percentage of total appointments'),
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
                    html.Td('Subject'),
                    html.Td(selected_subject),
                ]),
                html.Tr(children=[
                    html.Td(str(name) + ' amount'),
                    html.Td(df[subject].nunique()),
                ]),
                html.Tr(children=[
                    html.Td('Total appointments'),
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
                    html.Td('Appointments'),
                    html.Td(fraction),
                ]),
                html.Tr(children=[
                    html.Td('Percentage of total appointments'),
                    html.Td(percentage),
                ]),
            ]),
            html.Br(),
            html.Div(id='p-century-table'),
        ])


# Subject information table
@app.callback(
    Output('p-century-table', 'children'),
    Input('p-subject-dropdown', 'value'),
)
def update_timeline_table(selected_subject):
    df, subject, name = professorfigures.get_variables(selected_subject)
    table_df = professorfigures.create_century_table(df, name)
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


# Geographical information callbacks
# Geo input sync
@app.callback(
    Output('p-geo-min-input', 'value'),
    Output('p-geo-max-input', 'value'),
    Input('p-geo-min-input', 'value'),
    Input('p-geo-max-input', 'value'),
)
def synchronise_dates(min_year, max_year):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == 'p-geo-min-input' and min_year >= max_year:
        if max_year < data.all_dates_df['year'].max():
            max_year = min_year + 1
        else:
            min_year -= 1
    elif trigger_id == 'p-geo-max-input' and max_year <= min_year:
        if min_year > data.all_dates_df['year'].min():
            min_year = max_year - 1
        else:
            max_year += 1
    return min_year, max_year


# TODO: add option to show other subjects in geographical map
# Geo map
@app.callback(
    Output('p-map-container', 'children'),
    Output('p-map-table-container', 'children'),
    Input('p-geo-min-input', 'value'),
    Input('p-geo-max-input', 'value'),
    Input('p-map-choice', 'value'),
)
def create_map(min_year, max_year, map_choice):
    if map_choice == 'Heat map':
        figure, geo_data = professorfigures.create_country_map(min_year, max_year)
        geo_data = geo_data[['country', 'count']]
    elif map_choice == 'Line map':
        figure, geo_data = professorfigures.create_country_line_map(min_year, max_year)
        geo_data = geo_data[['country', 'count']]
    elif map_choice == 'MP Heat map':
        figure, geo_data = professorfigures.create_mapbox_heat_map(min_year, max_year)
        geo_data = geo_data[['country', 'count']]
    elif map_choice == 'MP Scatter map':
        figure, geo_data = professorfigures.create_mapbox_scatter_map(min_year, max_year)
        geo_data = geo_data[['country', 'year', 'count']]
    elif map_choice == 'Animated map':
        figure, geo_data = professorfigures.create_animated_country_map(min_year, max_year)
        geo_data = geo_data[['country', 'year', 'count']]
    else:
        figure, geo_data = professorfigures.create_country_map(min_year, max_year)
        geo_data = geo_data[['country', 'count']]
    geo_table = dash_table.DataTable(
        data=geo_data.to_dict('records'),
        columns=[{'id': i, 'name': i} for i in geo_data.columns],
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_size=100,
        fixed_rows={'headers': True},
        style_cell={
            'width': '{}%'.format(len(geo_data.columns)),
            'textOverflow': 'ellipsis',
            'overflow': 'hidden'
        },
        style_table={'overflowY': 'auto', 'overflowX': 'auto'},
        style_header={'backgroundColor': '#001158', 'color': 'white'},
        style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'white', 'color': 'black'},
        virtualization=True,
        id='p-geo-map-table'
    )
    return dcc.Graph(figure=figure, id='p-geo-map'), geo_table


# Individual information callbacks
# Individual table
@app.callback(
    Output('p-individual-search-results-number', 'children'),
    Output('p-individual-search-text', 'children'),
    Output('p-individual-table-container', 'children'),
    Input('p-search-individual', 'n_clicks'),
    Input('p-search-name', 'value'),
    Input('p-search-option', 'value'),
    Input('appointment-min-input', 'value'),
    Input('appointment-max-input', 'value'),
    Input('p-birthyear-min-input', 'value'),
    Input('p-birthyear-max-input', 'value'),
    Input('p-include-missing-dates', 'value'),
    Input('p-individual-gender-dropdown', 'value'),
    Input('p-individual-birthplace-dropdown', 'value'),
    Input('p-individual-birthcountry-dropdown', 'value'),
    Input('p-individual-deathplace-dropdown', 'value'),
    Input('p-individual-deathcountry-dropdown', 'value'),
    Input('p-individual-promotion-dropdown', 'value'),
    Input('p-individual-promotionplace-dropdown', 'value'),
    Input('p-individual-thesis-dropdown', 'value'),
    Input('p-individual-job-dropdown', 'value'),
    Input('p-individual-subjectarea-dropdown', 'value'),
    Input('p-individual-faculty-dropdown', 'value'),
    )
def update_student_table(search_button, selected_name, search_option, min_enrol, max_enrol, min_birth, max_birth,
                         include_missing, selected_gender, selected_birthplace, selected_birthcountry,
                         selected_deathplace, selected_deathcountry, selected_promotion, selected_promotionplace,
                         selected_thesis, selected_job, selected_subjectarea, selected_faculty):
    df = data.individual_profs_df[['First name', 'Last name', 'Gender', 'Appointment date', 'Appointment year',
                                   'Birth date', 'Birth year', 'Birth place', 'Birth country', 'Death date'
                                   'Death year', 'Death place', 'Death country', 'Promotion', 'Promotion place',
                                   'Promotion date', 'Promotion year', 'Thesis', 'Job', 'Subject area', 'Faculty',
                                   'Rating']]
    text = 'professors were found'
    search_results_number = 0
    if ctx.triggered_id == 'p-search-individual':
        filtered_df = df
        if selected_name is not None and selected_name != '':
            words = selected_name.split(' ')
            temp_total_df = pd.DataFrame()
            for word in words:
                if search_option == 'Contains':
                    temp_df = df[df['First name'].str.contains(word)]
                    if len(temp_df) > 0:
                        temp_total_df = pd.concat((temp_total_df, temp_df), axis=0).drop_duplicates()
                    temp_df = df[df['Last name'].str.contains(word)]
                    if len(temp_df) > 0:
                        temp_total_df = pd.concat((temp_total_df, temp_df), axis=0).drop_duplicates()
                elif search_option == 'Equals':
                    temp_df = df.loc[df['First name'] == word]
                    if len(temp_df) > 0:
                        temp_total_df = pd.concat((temp_total_df, temp_df), axis=0).drop_duplicates()
                    temp_df = df.loc[df['Last name'] == word]
                    if len(temp_df) > 0:
                        temp_total_df = pd.concat((temp_total_df, temp_df), axis=0).drop_duplicates()
            if len(temp_total_df) > 0:
                filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            else:
                filtered_df = pd.DataFrame(
                    columns=['First name', 'Last name', 'Gender', 'Appointment date', 'Appointment year', 'Birth date',
                                   'Birth year', 'Birth place', 'Birth country', 'Death date', 'Death year',
                                   'Death place', 'Death country', 'Promotion', 'Promotion place', 'Promotion date',
                                   'Promotion year', 'Thesis', 'Job', 'Subject area', 'Faculty', 'Rating'])
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['First name'].isnull()]
                temp_missing_df = pd.concat((temp_missing_df, df.loc[df['Last name'].isnull()]),
                                            axis=0).drop_duplicates()
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if min_enrol is not None and max_enrol is not None:
            filtered_df = filtered_df.loc[filtered_df['Appointment year'] <= int(max_enrol)]
            filtered_df = filtered_df[filtered_df['Appointment year'] >= int(min_enrol)]
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Appointment year'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if min_birth is not None and max_enrol is not None:
            filtered_df = filtered_df.loc[filtered_df['Birth year'] <= int(max_birth)]
            filtered_df = filtered_df[filtered_df['Birth year'] >= int(min_birth)]
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Birth year'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_gender is not None and selected_gender != []:
            temp_total_df = pd.DataFrame()
            for c in selected_gender:
                temp_df = df.loc[df['Gender'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Gender'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_birthplace is not None and selected_birthplace != []:
            temp_total_df = pd.DataFrame()
            for c in selected_birthplace:
                temp_df = df.loc[df['Birth place'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Birth place'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_birthcountry is not None and selected_birthcountry != []:
            temp_total_df = pd.DataFrame()
            for c in selected_birthcountry:
                temp_df = df.loc[df['Birth country'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Birth country'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_deathplace is not None and selected_deathplace != []:
            temp_total_df = pd.DataFrame()
            for c in selected_deathplace:
                temp_df = df.loc[df['Death place'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Death place'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_deathcountry is not None and selected_deathcountry != []:
            temp_total_df = pd.DataFrame()
            for c in selected_deathcountry:
                temp_df = df.loc[df['Death country'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Death country'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_promotion is not None and selected_promotion != []:
            temp_total_df = pd.DataFrame()
            for c in selected_promotion:
                temp_df = df.loc[df['Promotion'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Promotion'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_promotionplace is not None and selected_promotionplace != []:
            temp_total_df = pd.DataFrame()
            for c in selected_promotionplace:
                temp_df = df.loc[df['Promotion place'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Promotion place'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_thesis is not None and selected_thesis != []:
            temp_total_df = pd.DataFrame()
            for c in selected_thesis:
                temp_df = df.loc[df['Thesis'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Thesis'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_job is not None and selected_job != []:
            temp_total_df = pd.DataFrame()
            for c in selected_job:
                temp_df = df.loc[df['Job'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Job'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_subjectarea is not None and selected_subjectarea != []:
            temp_total_df = pd.DataFrame()
            for c in selected_subjectarea:
                temp_df = df.loc[df['Subject area'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Subject area'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_faculty is not None and selected_faculty != []:
            temp_total_df = pd.DataFrame()
            for c in selected_faculty:
                temp_df = df.loc[df['Faculty'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Faculty'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        search_results_number = len(filtered_df)
        return search_results_number, text, dash_table.DataTable(
            data=filtered_df.to_dict('records'),
            columns=[{'id': i, 'name': i, 'hideable': 'last'} for i in filtered_df.columns],
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable='single',
            row_selectable='multi',
            selected_columns=[],
            selected_rows=[],
            page_size=100,
            fixed_rows={'headers': True},
            style_cell={
                'width': '7%',
                'textOverflow': 'ellipsis',
                'overflow': 'hidden'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'First name'},
                 'width': '10%'},
                {'if': {'column_id': 'Last name'},
                 'width': '10%'},
            ],
            style_header={'backgroundColor': '#001158', 'color': 'white'},
            style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'white', 'color': 'black'},
            virtualization=True,
            #            export_format='xlsx',
            #            export_headers='display',
            merge_duplicate_headers=True,
            id='p-individual-table'
        )
    # else: return None, None, None


# Chosen person information
@app.callback(
    Output('p-chosen-individual-information', 'children'),
    Input('p-individual-table', "derived_virtual_data"),
    Input('p-individual-table', "derived_virtual_selected_rows"),
    Input({'type': 'p-person-table', 'index': ALL}, 'id'),
    State('p-chosen-individual-information', 'children'),
    )
def create_individual_information(rows, selected_rows, value, children):
    if rows is None:
        persons = 'No person selected'
    else:
        persons = pd.DataFrame(rows)
    in_list = []
    for v in value:
        if v['index'] not in selected_rows:
            counter = 0
            for child in children:
                if v['index'] == child['props']['id']['index']:
                    children.remove(child)
                counter += 1
        else:
            in_list.append(v['index'])
    for number in selected_rows:
        if number not in in_list:
            person = persons.iloc[number].to_frame().T
            figure = professorfigures.create_map(person['Birth place'][number], person['Birth country'][number],
                                                 person['Birth year'][number])
            new_person = html.Div(id={'type': 'p-person-table', 'index': number}, className='bigblock',
                                  children=[
                                      html.Table(className='block',
                                                 style={'border': '1px solid black', 'border-collapse': 'collapse'},
                                                 children=[
                                                     html.Tr(children=[
                                                         html.Td('First name:'),
                                                         html.Td(person.get('First name')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Last name:'),
                                                         html.Td(person.get('Last name')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Birth date:'),
                                                         html.Td(person.get('Birth date')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Death date:'),
                                                         html.Td(person.get('Death date')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Promotion:'),
                                                         html.Td(person.get('Promotion')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Promotion:'),
                                                         html.Td(person.get('Promotion date')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Thesis:'),
                                                         html.Td(person.get('Thesis')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Appointment date:'),
                                                         html.Td(person.get('Appointment date')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Job:'),
                                                         html.Td(person.get('Job')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Subject area:'),
                                                         html.Td(person.get('Subject area')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Faculty:'),
                                                         html.Td(person.get('')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Oration:'),
                                                         html.Td(person.get('Oration')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Oration date:'),
                                                         html.Td(person.get('Oration date')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('End of employment:'),
                                                         html.Td(person.get('End of employment')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Reason:'),
                                                         html.Td(person.get('Reason')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Details:'),
                                                         html.Td(person.get('Details')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Rating:'),
                                                         html.Td(person.get('Rating')),
                                                     ]),
                                                 ]),
                                      html.Table(className='block', children=[
                                          html.Tr(children=[
                                              html.Td('Birth place:'),
                                              html.Td(person.get('Birth place')),
                                          ]),
                                          html.Tr(children=[
                                              html.Td('Birth country:'),
                                              html.Td(person.get('Birth country')),
                                          ]),
                                          html.Tr(children=[
                                              html.Td('Promotion place:'),
                                              html.Td(person.get('Promotion place')),
                                          ]),
                                          html.Tr(children=[
                                              html.Td('Death place:'),
                                              html.Td(person.get('Death place')),
                                          ]),
                                          html.Tr(children=[
                                              html.Td('Death country:'),
                                              html.Td(person.get('Death country')),
                                          ]),
                                      ]),
                                      # html.A('Go to globe', href='assets/mapboxLeiden.html', target='_blank', rel='noreferrer noopener'),
                                      # TODO: Implement family tree, not yet chosen which
                                      #  tree fits best: choices: 1. fisher_crawford (r implementation) 2. graphviz
                                      #  3. igraph
                                      dcc.Graph(figure=figure, id='p-life-map')
                                  ])
            children.append(new_person)
    return children


# Appointment input sync
@app.callback(
    Output('appointment-min-input', 'value'),
    Output('appointment-max-input', 'value'),
    Input('appointment-min-input', 'value'),
    Input('appointment-max-input', 'value'),
    )
def synchronise_dates(min_year, max_year):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == 'appointment-min-input' and min_year >= max_year:
        if max_year < data.all_dates_df['year'].max():
            max_year = min_year + 1
        else:
            min_year -= 1
    elif trigger_id == 'appointment-max-input' and max_year <= min_year:
        if min_year > data.all_dates_df['year'].min():
            min_year = max_year - 1
        else:
            max_year += 1
    return min_year, max_year


# Birthyear input sync
@app.callback(
    Output('p-birthyear-min-input', 'value'),
    Output('p-birthyear-max-input', 'value'),
    Input('p-birthyear-min-input', 'value'),
    Input('p-birthyear-max-input', 'value'),
    )
def synchronise_dates(min_year, max_year):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == 'p-birthyear-min-input' and min_year >= max_year:
        if max_year < data.all_dates_df['year'].max():
            max_year = min_year + 1
        else:
            min_year -= 1
    elif trigger_id == 'p-birthyear-max-input' and max_year <= min_year:
        if min_year > data.all_dates_df['year'].min():
            min_year = max_year - 1
        else:
            max_year += 1
    return min_year, max_year

###################################################################### 
# Students callbacks
###################################################################### 
# Year slider


@app.callback(
    Output('year-slider', 'min'),
    Output('year-slider', 'max'),
    Output('year-slider', 'value'),
    Output('year-slider', 'marks'),
    Input('year-century-slider', 'value')
)
def update_year_slider(century):
    current_century = data.all_dates_df[(data.all_dates_df['century'] <= century[-1])]
    years = []
    for y in current_century['year'][0::YEAR_STEP]:
        years.append(y)
    years.append(current_century['year'].max())
    min = current_century['year'].min()
    max = current_century['year'].max()
    value = [current_century['year'].min(), current_century['year'].max()]
    marks = {str(year): str(year) for year in 
              range(current_century['year'].min(), current_century['year'].max(),
              int((current_century['year'].max() - current_century['year'].min()) / MARK_SPACING )) }
    id = 'year-slider'
    return min, max, value, marks


# year-century graph
@app.callback(
    Output('year-century-dropdown-container', 'children'),
    Input('year-century-subject-dropdown', 'value'),
    Input('year-century-slider', 'value'),
    Input('year-slider', 'value'),
    Input('subject-slider', 'value'),
    Input('year-century-dropdown', 'value'),
    running=[
        (Output('year-century-subject-dropdown', 'disabled'), True, False),
    ],
)
def update_year_century_output(selected_subject, selected_century, selected_year, selected_age, selected_dropdown):
    return dcc.Graph(figure=studentfigures.create_year_cent_figure(selected_subject, selected_century, selected_year,
                                                                   selected_age, selected_dropdown),
                     id='year-century-graph')


# century-graph
@app.callback(
    Output('century-dropdown-container', 'children'),
    Input('year-century-subject-dropdown', 'value'),
    Input('year-century-slider', 'value'),
)
def update_century_output(selected_subject, selected_century):
    return dcc.Graph(figure=studentfigures.create_cent_figure(selected_subject, selected_century), id='century-graph')


# Timeline information
@app.callback(
    Output('timeline-information', 'children'),
    Input('year-century-subject-dropdown', 'value'),
    Input('year-century-graph', 'hoverData'),
    Input('year-century-graph', 'figure'),
)
def update_timeline_information(selected_subject, hover_data, figure):
    if hover_data is not None:
        text = hover_data['points'][0]['hovertext']
        y = hover_data['points'][0]['x']
        year = int(y)
    else:
        text = None
        year = figure['data'][0]['x'][0]
    df, subject, name = studentfigures.get_variables(selected_subject)
    century = df.loc[df['year'] == year, 'century'].values[0]
    enrollments = df.loc[df['year'] == year, 'count'].values[0]
    last_year = year - 1
    if last_year in figure['data'][0]['x']:
        last_year_enrollments = df.loc[df['year'] == last_year, 'count'].values[0]
        growth = enrollments - last_year_enrollments
    else:
        growth = 'No data'
    if subject == 'year':
        return html.Table(id='timeline-table', children=[
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
                html.Td('Enrollments'),
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
                html.Td('Total Enrollments'),
                html.Td(df['count'].sum()),
            ]),
            html.Tr(children=[
                html.Td('Most enrollments'),
                html.Td(df['count'].max()),
            ]),
            html.Tr(children=[
                html.Td('Highest Year'),
                html.Td(df.loc[df['count'] == df['count'].max(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Least enrollments'),
                html.Td(df['count'].min()),
            ]),
            html.Tr(children=[
                html.Td('Lowest Year'),
                html.Td(df.loc[df['count'].min(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Average Enrollments'),
                html.Td(round(df['count'].mean(),0)),
            ]),
        ]),
    else:
        return html.Table(id='timeline-table', children=[
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
                html.Td('Enrollments'),
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
                html.Td('Total Enrollments'),
                html.Td(df['count'].sum()),
            ]),
            html.Tr(children=[
                html.Td('Most enrollments'),
                html.Td(df['count'].max()),
            ]),
            html.Tr(children=[
                html.Td('Highest Year'),
                html.Td(df.loc[df['count'] == df['count'].max(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Least enrollments'),
                html.Td(df['count'].min()),
            ]),
            html.Tr(children=[
                html.Td('Lowest Year'),
                html.Td(df.loc[df['count'].min(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Average Enrollments'),
                html.Td(round(df['count'].mean(),0)),
            ]),
        ]),


# Subject information callbacks
# Subject-graph
@app.callback(
    Output('subject-dropdown-container', 'children'),
    Input('subject-dropdown', 'value'),
    running=[
        (Output('subject-dropdown', 'disabled'), True, False),
    ],
)
def update_subject_output(selected_subject):
    return dcc.Graph(figure=studentfigures.create_subject_info_graph(selected_subject), id='subject-graph')


# Subject table
@app.callback(
    Output('subject-table-container', 'children'),
    Input('subject-dropdown', 'value'),
)
def update_timeline_table(selected_subject):
    df, subject, name = studentfigures.get_variables(selected_subject)
    df = df.rename(columns={subject: name, 'year': 'Year', 'count': 'Enrollments', 'century': 'Century'})
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
#        export_format='xlsx',
#        export_headers='display',
        merge_duplicate_headers=True,
        id='subject-table'
    )


# Subject information
@app.callback(
    Output('subject-information', 'children'),
    Input('subject-dropdown', 'value'),
    Input('subject-graph', 'hoverData'),
)
def update_timeline_information(selected_subject, hover_data):
    if hover_data is not None:
        text = hover_data['points'][0]['hovertext']
    else:
        text = None
    df, subject, name = studentfigures.get_variables(selected_subject)
    total = df['count'].sum()
    fraction = df.loc[df[subject] == text, 'count'].sum()
    percentage = round(fraction / total * 100, 2)
    if subject == 'year':
        return html.Div(id='subject-hover-info', children=[
            html.Table(id='subject-table', children=[
                html.Tr(children=[
                    html.Td('Subject'),
                    html.Td(selected_subject),
                ]),
                html.Tr(children=[
                    html.Td(str(name) + ' amount'),
                    html.Td(df[subject].nunique()),
                ]),
                html.Tr(children=[
                    html.Td('Total enrollments'),
                    html.Td(total),
                ]),
                html.Tr(children=[
                    html.Td('Average enrollments per year'),
                    html.Td(html.Td(round(df['count'].mean(), 0))),
                ]),
                html.Tr(children=[
                    html.Td('Year with most enrollments'),
                    html.Td(df.loc[df['count'] == df['count'].max(), subject].unique()),
                ]),
                html.Tr(children=[
                    html.Td('Year with least enrollments'),
                    html.Td(df.loc[df['count'] == df['count'].min(), subject].unique()),
                ]),
            ]),
            html.Br(),
            html.Table(id='chosen-subject-table', children=[
                html.Tr(children=[
                    html.Td('Year'),
                    html.Td(text),
                ]),
                html.Tr(children=[
                    html.Td('Enrollments'),
                    html.Td(fraction),
                ]),
                html.Tr(children=[
                    html.Td('Percentage of total enrollments'),
                    html.Td(percentage),
                ]),
            ]),
            html.Br(),
            html.Div(id='century-table'),
        ])
    else:
        return html.Div(id='subject-hover-info', children=[
            html.Table(id='subject-table', children=[
                html.Tr(children=[
                    html.Td('Subject'),
                    html.Td(selected_subject),
                ]),
                html.Tr(children=[
                    html.Td(str(name) + ' amount'),
                    html.Td(df[subject].nunique()),
                ]),
                html.Tr(children=[
                    html.Td('Total enrollments'),
                    html.Td(total),
                ]),
                html.Tr(children=[
                    html.Td('Average yearly enrollments per ' + str(subject)),
                    html.Td(html.Td(round(df['count'].mean(), 0))),
                ]),
                html.Tr(children=[
                    html.Td(str(name) + ' with most enrollments in one year'),
                    html.Td(df.loc[df['count'] == df['count'].max(), subject].unique()),
                ]),
                html.Tr(children=[
                    html.Td(str(name) + ' with least enrollments in one year'),
                    html.Td(df.loc[df['count'] == df['count'].min(), subject].unique()[0]),
                ]),
            ]),
            html.Br(),
            html.Table(id='chosen-subject-table', children=[
                html.Tr(children=[
                    html.Th(name),
                    html.Th(text),
                ]),
                html.Tr(children=[
                    html.Td('Enrollments'),
                    html.Td(fraction),
                ]),
                html.Tr(children=[
                    html.Td('Percentage of total enrollments'),
                    html.Td(percentage),
                ]),
            ]),
            html.Br(),
            html.Div(id='century-table'),
        ])


# Subject information table
@app.callback(
    Output('century-table', 'children'),
    Input('subject-dropdown', 'value'),
)
def update_timeline_table(selected_subject):
    df, subject, name = studentfigures.get_variables(selected_subject)
    table_df = studentfigures.create_century_table(df, name)
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
        id='subject-information-table'
    )


# Geographical information callbacks
# Geo input sync
@app.callback(
    Output('geo-min-input', 'value'),
    Output('geo-max-input', 'value'),
    Input('geo-min-input', 'value'),
    Input('geo-max-input', 'value'),
)
def synchronise_dates(min_year, max_year):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == 'geo-min-input' and min_year >= max_year:
        if max_year < data.year_df['year'].max():
            max_year = min_year + 1
        else:
            min_year -= 1
    elif trigger_id == 'geo-max-input' and max_year <= min_year:
        if min_year > data.year_df['year'].min():
            min_year = max_year - 1
        else:
            max_year += 1
    return min_year, max_year


# TODO: add option to show other subjects in geographical map
# Geo map
@app.callback(
    Output('map-container', 'children'),
    Output('map-table-container', 'children'),
    Input('geo-min-input', 'value'),
    Input('geo-max-input', 'value'),
    Input('map-choice', 'value'),
)
def create_map(min_year, max_year, map_choice):
    if map_choice == 'Heat map':
        figure, geo_data = studentfigures.create_country_map(min_year, max_year)
        geo_data = geo_data[['country', 'count']]
    elif map_choice == 'Line map':
        figure, geo_data = studentfigures.create_country_line_map(min_year, max_year)
        geo_data = geo_data[['country', 'count']]
    elif map_choice == 'MP Heat map':
        figure, geo_data = studentfigures.create_mapbox_heat_map(min_year, max_year)
        geo_data = geo_data[['country', 'count']]
    elif map_choice == 'MP Scatter map':
        figure, geo_data = studentfigures.create_mapbox_scatter_map(min_year, max_year)
        geo_data = geo_data[['country', 'year', 'count']]
    elif map_choice == 'Animated map':
        figure, geo_data = studentfigures.create_animated_country_map(min_year, max_year)
        geo_data = geo_data[['country', 'year', 'count']]
    else:
        figure, geo_data = studentfigures.create_country_map(min_year, max_year)
        geo_data = geo_data[['country', 'count']]
    geo_table = dash_table.DataTable(
        data=geo_data.to_dict('records'),
        columns=[{'id': i, 'name': i} for i in geo_data.columns],
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_size=100,
        fixed_rows={'headers': True},
        style_cell={
            'width': '{}%'.format(len(geo_data.columns)),
            'textOverflow': 'ellipsis',
            'overflow': 'hidden'
        },
        style_table={'overflowY': 'auto', 'overflowX': 'auto'},
        style_header={'backgroundColor': '#001158', 'color': 'white'},
        style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'white', 'color': 'black'},
        virtualization=True,
        id='geo-map-table'
    )
    return dcc.Graph(figure=figure, id='geo-map'), geo_table


# Individual information callbacks
# Individual table
@app.callback(
    Output('individual-search-results-number', 'children'),
    Output('individual-search-text', 'children'),
    Output('individual-table-container', 'children'),
    Input('search-individual', 'n_clicks'),
    Input('search-name', 'value'),
    Input('search-option', 'value'),
    Input('enrollment-min-input', 'value'),
    Input('enrollment-max-input', 'value'),
    Input('birthyear-min-input', 'value'),
    Input('birthyear-max-input', 'value'),
    Input('include-missing-dates', 'value'),
    Input('individual-age-slider', 'value'),
    Input('individual-city-dropdown', 'value'),
    Input('individual-country-dropdown', 'value'),
    Input('individual-region-dropdown', 'value'),
    Input('individual-faculty-dropdown', 'value'),
    Input('individual-royal-dropdown', 'value'),
    Input('individual-job-dropdown', 'value'),
    Input('individual-religion-dropdown', 'value'),
)
def update_student_table(search_button, selected_name, search_option, min_enrol, max_enrol, min_birth, max_birth,
                         include_missing,
                         selected_age, selected_city, selected_country, selected_region, selected_faculty,
                         selected_royal, selected_job, selected_religion):
    df = data.individual_df[['First name', 'Last name', 'Enrollment year', 'City', 'Country', 'Region',
                             'Enrollment age', 'Birth year', 'Faculty', 'Royal title', 'Job', 'Religion',
                             'Enrollments', 'Rating']]
    text = 'students were found'
    search_results_number = 0
    if ctx.triggered_id == 'search-individual':
        filtered_df = df
        if selected_name is not None and selected_name != '':
            words = selected_name.split(' ')
            temp_total_df = pd.DataFrame()
            for word in words:
                if search_option == 'Contains':
                    temp_df = df[df['First name'].str.contains(word)]
                    if len(temp_df) > 0:
                        temp_total_df = pd.concat((temp_total_df, temp_df), axis=0).drop_duplicates()
                    temp_df = df[df['Last name'].str.contains(word)]
                    if len(temp_df) > 0:
                        temp_total_df = pd.concat((temp_total_df, temp_df), axis=0).drop_duplicates()
                elif search_option == 'Equals':
                    temp_df = df.loc[df['First name'] == word]
                    if len(temp_df) > 0:
                        temp_total_df = pd.concat((temp_total_df, temp_df), axis=0).drop_duplicates()
                    temp_df = df.loc[df['Last name'] == word]
                    if len(temp_df) > 0:
                        temp_total_df = pd.concat((temp_total_df, temp_df), axis=0).drop_duplicates()
            if len(temp_total_df) > 0:
                filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            else:
                filtered_df = pd.DataFrame(columns=['First name', 'Last name', 'Enrollment year', 'City', 'Country',
                                                    'Region', 'Enrollment age', 'Birth year', 'Faculty', 'Royal title',
                                                    'Job', 'Religion', 'Enrollments', 'Rating'])
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['First name'].isnull()]
                temp_missing_df = pd.concat((temp_missing_df, df.loc[df['Last name'].isnull()]),
                                            axis=0).drop_duplicates()
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if min_enrol is not None and max_enrol is not None:
            filtered_df = filtered_df.loc[filtered_df['Enrollment year'] <= int(max_enrol)]
            filtered_df = filtered_df[filtered_df['Enrollment year'] >= int(min_enrol)]
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Enrollment year'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if min_birth is not None and max_enrol is not None:
            filtered_df = filtered_df.loc[filtered_df['Birth year'] <= int(max_birth)]
            filtered_df = filtered_df[filtered_df['Birth year'] >= int(min_birth)]
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Birth year'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_age is not None:
            filtered_df = filtered_df.loc[filtered_df['Enrollment age'] <= int(selected_age[1])]
            filtered_df = filtered_df[filtered_df['Enrollment age'] >= int(selected_age[0])]
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Enrollment age'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_city is not None and selected_city != []:
            temp_total_df = pd.DataFrame()
            for c in selected_city:
                temp_df = df.loc[df['City'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['City'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_country is not None and selected_country != []:
            temp_total_df = pd.DataFrame()
            for c in selected_country:
                temp_df = df.loc[df['Country'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Country'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_region is not None and selected_region != []:
            temp_total_df = pd.DataFrame()
            for c in selected_region:
                temp_df = df.loc[df['Region'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Region'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_faculty is not None and selected_faculty != []:
            temp_total_df = pd.DataFrame()
            for c in selected_faculty:
                temp_df = df.loc[df['Faculty'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Faculty'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_royal is not None and selected_royal != []:
            temp_total_df = pd.DataFrame()
            for c in selected_royal:
                temp_df = df.loc[df['Royal title'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Royal title'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_job is not None and selected_job != []:
            temp_total_df = pd.DataFrame()
            for c in selected_job:
                temp_df = df.loc[df['Job'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Job'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if selected_religion is not None and selected_religion != []:
            temp_total_df = pd.DataFrame()
            for c in selected_religion:
                temp_df = df.loc[df['Religion'] == c]
                temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
            filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Religion'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        filtered_df = filtered_df.rename(columns={'Enrollment year': 'Year', 'Enrollment age': 'Age'})
        search_results_number = len(filtered_df)
        return search_results_number, text, dash_table.DataTable(
            data=filtered_df.to_dict('records'),
            columns=[{'id': i, 'name': i, 'hideable': 'last'} for i in filtered_df.columns],
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable='single',
            row_selectable='multi',
            selected_columns=[],
            selected_rows=[],
            page_size=100,
            fixed_rows={'headers': True},
            style_cell={
                'width': '7%',
                'textOverflow': 'ellipsis',
                'overflow': 'hidden'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'First name'},
                 'width': '10%'},
                {'if': {'column_id': 'Last name'},
                 'width': '10%'},
                {'if': {'column_id': 'City'},
                 'width': '5%'},
                {'if': {'column_id': 'Country'},
                 'width': '6%'},
                {'if': {'column_id': 'Region'},
                 'width': '6%'},
                {'if': {'column_id': 'Year'},
                 'width': '5%'},
                {'if': {'column_id': 'Age'},
                 'width': '5%'},
                {'if': {'column_id': 'Birth year'},
                 'width': '8%'},
                {'if': {'column_id': 'Faculty'},
                 'width': '7%'},
                {'if': {'column_id': 'Royal title'},
                 'width': '9%'},
                {'if': {'column_id': 'Job'},
                 'width': '5%'},
                {'if': {'column_id': 'Religion'},
                 'width': '9%'},
                {'if': {'column_id': 'Enrollments'},
                 'width': '10%'},
                {'if': {'column_id': 'Rating'},
                 'width': '5%'}
            ],
            style_header={'backgroundColor': '#001158', 'color': 'white'},
            style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'white', 'color': 'black'},
            virtualization=True,
#            export_format='xlsx',
#            export_headers='display',
            merge_duplicate_headers=True,
            id='individual-table'
        )
    # else: return None, None, None


# Chosen person information
@app.callback(
    Output('chosen-individual-information', 'children'),
    Input('individual-table', "derived_virtual_data"),
    Input('individual-table', "derived_virtual_selected_rows"),
    Input({'type': 'person-table', 'index': ALL}, 'id'),
    State('chosen-individual-information', 'children'),
)
def create_individual_information(rows, selected_rows, value, children):
    if rows is None:
        persons = 'No person selected'
    else:
        persons = pd.DataFrame(rows)
    in_list = []
    for v in value:
        if v['index'] not in selected_rows:
            counter = 0
            for child in children:
                if v['index'] == child['props']['id']['index']:
                    children.remove(child)
                counter += 1
        else:
            in_list.append(v['index'])
    for number in selected_rows:
        if number not in in_list:
            person = persons.iloc[number].to_frame().T
            figure = studentfigures.create_map(person['City'][number], person['Country'][number],
                                               person['Birth year'][number])
            new_person = html.Div(id={'type': 'person-table', 'index': number}, className='bigblock',
                                  children=[
                                      html.Table(className='block',
                                                 style={'border': '1px solid black', 'border-collapse': 'collapse'},
                                                 children=[
                                                     html.Tr(children=[
                                                         html.Td('First name:'),
                                                         html.Td(person.get('First name')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Last name:'),
                                                         html.Td(person.get('Last name')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Birth year:'),
                                                         html.Td(person.get('Birth year')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Honorary title:'),
                                                         html.Td(person.get('Honor')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Royal title:'),
                                                         html.Td(person.get('Royal title')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Enrollment day:'),
                                                         html.Td(person.get('Enrollment day')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Enrollment month:'),
                                                         html.Td(person.get('Enrollment month')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Enrollment year:'),
                                                         html.Td(person.get('Enrollment year')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Enrollment age:'),
                                                         html.Td(person.get('Enrollment age')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Faculty:'),
                                                         html.Td(person.get('Faculty')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Job:'),
                                                         html.Td(person.get('Job')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Religion:'),
                                                         html.Td(person.get('Religion')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Extra:'),
                                                         html.Td(person.get('Extra')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Remark:'),
                                                         html.Td(person.get('Remark')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Previous enrollment:'),
                                                         html.Td(person.get('Previous enrollment')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Previous faculty:'),
                                                         html.Td(person.get('Previous faculty')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Original faculty:'),
                                                         html.Td(person.get('Original faculty')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Rating:'),
                                                         html.Td(person.get('Rating')),
                                                     ]),
                                                 ]),
                                      html.Table(className='block', children=[
                                          html.Tr(children=[
                                              html.Td('City:'),
                                              html.Td(person.get('City')),
                                          ]),
                                          html.Tr(children=[
                                              html.Td('Country:'),
                                              html.Td(person.get('Country')),
                                          ]),
                                          html.Tr(children=[
                                              html.Td('Region:'),
                                              html.Td(person.get('Region')),
                                          ]),
                                      ]),
                                      # html.A('Go to globe', href='assets/mapboxLeiden.html', target='_blank', rel='noreferrer noopener'),
                                      # TODO: Implement family tree, not yet chosen which
                                      #  tree fits best: choices: 1. fisher_crawford (r implementation) 2. graphviz
                                      #  3. igraph
                                      dcc.Graph(figure=figure, id='life-map')
                                  ])
            children.append(new_person)
    return children


# Enrollment input sync
@app.callback(
    Output('enrollment-min-input', 'value'),
    Output('enrollment-max-input', 'value'),
    Input('enrollment-min-input', 'value'),
    Input('enrollment-max-input', 'value'),
)
def synchronise_dates(min_year, max_year):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == 'enrollment-min-input' and min_year >= max_year:
        if max_year < data.year_df['year'].max():
            max_year = min_year + 1
        else:
            min_year -= 1
    elif trigger_id == 'enrollment-max-input' and max_year <= min_year:
        if min_year > data.year_df['year'].min():
            min_year = max_year - 1
        else:
            max_year += 1
    return min_year, max_year


# Birthyear input sync
@app.callback(
    Output('birthyear-min-input', 'value'),
    Output('birthyear-max-input', 'value'),
    Input('birthyear-min-input', 'value'),
    Input('birthyear-max-input', 'value'),
)
def synchronise_dates(min_year, max_year):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == 'birthyear-min-input' and min_year >= max_year:
        if max_year < data.year_df['year'].max():
            max_year = min_year + 1
        else:
            min_year -= 1
    elif trigger_id == 'birthyear-max-input' and max_year <= min_year:
        if min_year > data.year_df['year'].min():
            min_year = max_year - 1
        else:
            max_year += 1
    return min_year, max_year

###################################################################### 
# Rector callbacks
###################################################################### 
# Year slider
@app.callback(
    Output('r-year-slider', 'min'),
    Output('r-year-slider', 'max'),
    Output('r-year-slider', 'value'),
    Output('r-year-slider', 'marks'),
    Input('r-year-century-slider', 'value')
)
def update_year_slider(century):
    current_century = data.all_dates_df[(data.all_dates_df['century'] <= century[-1])]
    years = []
    for y in current_century['year'][0::YEAR_STEP]:
        years.append(y)
    years.append(current_century['year'].max())
    min = current_century['year'].min()
    max = current_century['year'].max()
    value = [current_century['year'].min(), current_century['year'].max()]
    marks = {str(year): str(year) for year in 
              range(current_century['year'].min(), current_century['year'].max(),
              int((current_century['year'].max() - current_century['year'].min()) / MARK_SPACING )) }
    id = 'r-year-slider'
    return min, max, value, marks


# year-century graph
@app.callback(
    Output('r-year-century-dropdown-container', 'children'),
    Input('r-year-century-subject-dropdown', 'value'),
    Input('r-year-century-slider', 'value'),
    Input('r-year-slider', 'value'),
    Input('r-year-century-dropdown', 'value'),
    running=[
        (Output('r-year-century-subject-dropdown', 'disabled'), True, False),
    ],
)
def r_update_year_century_output(selected_subject, selected_century, selected_year, selected_dropdown):
    return dcc.Graph(figure=rectorfigures.create_year_cent_figure(selected_subject, selected_century, selected_year,
                                                                  selected_dropdown),
                     id='r-year-century-graph')


# century-graph
@app.callback(
    Output('r-century-dropdown-container', 'children'),
    Input('r-year-century-subject-dropdown', 'value'),
    Input('r-year-century-slider', 'value'),
)
def r_update_century_output(selected_subject, selected_century):
    return dcc.Graph(figure=rectorfigures.create_cent_figure(selected_subject, selected_century), id='century-graph')


# Timeline information
@app.callback(
    Output('r-timeline-information', 'children'),
    Input('r-year-century-subject-dropdown', 'value'),
    Input('r-year-century-graph', 'hoverData'),
    Input('r-year-century-graph', 'figure'),
)
def r_update_timeline_information(selected_subject, hover_data, figure):
    if hover_data is not None:
        text = hover_data['points'][0]['hovertext']
        y = hover_data['points'][0]['x']
        year = int(y)
    else:
        text = None
        year = figure['data'][0]['x'][0]
    df, subject, name = rectorfigures.get_variables(selected_subject)
    century = df.loc[df['year'] == year, 'century'].values[0]
    rectors = df.loc[df['year'] == year, 'count'].values[0]
    last_year = year - 1
    if last_year in figure['data'][0]['x']:
        last_year_rectors = df.loc[df['year'] == last_year, 'count'].values[0]
        growth = rectors - last_year_rectors
    else:
        growth = 'No data'
    return html.Table(id='timeline-table', children=[
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
            html.Td('Rectors'),
            html.Td(rectors),
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
            html.Td('Total Rectors'),
            html.Td(df['count'].sum()),
        ]),
        html.Tr(children=[
            html.Td('Most Rectors'),
            html.Td(df['count'].max()),
        ]),
        html.Tr(children=[
            html.Td('Highest Year'),
            html.Td(df.loc[df['count'].max(), 'year']),
        ]),
        html.Tr(children=[
            html.Td('Least Rectors'),
            html.Td(df['count'].min()),
        ]),
        html.Tr(children=[
            html.Td('Lowest Year'),
            html.Td(df.loc[df['count'].min(), 'year']),
        ]),
        html.Tr(children=[
            html.Td('Average Rectors'),
            html.Td(round(df['count'].mean(),0)),
        ]),
    ]),


# Subject information callbacks
# Subject-graph
@app.callback(
    Output('r-subject-dropdown-container', 'children'),
    Input('r-subject-dropdown', 'value'),
    running=[
        (Output('r-subject-dropdown', 'disabled'), True, False),
    ],
)
def r_update_subject_output(selected_subject):
    return dcc.Graph(figure=rectorfigures.create_subject_info_graph(selected_subject), id='r-subject-graph')


# Subject table
@app.callback(
    Output('r-subject-table-container', 'children'),
    Input('r-subject-dropdown', 'value'),
)
def r_update_timeline_table(selected_subject):
    df, subject, name = rectorfigures.get_variables(selected_subject)
    df = df.rename(columns={subject: name, 'year': 'Year', 'count': 'Rectors', 'century': 'Century'})
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
 #       export_format='xlsx',
 #       export_headers='display',
        merge_duplicate_headers=True,
        id='r-subject-table'
    )


# Subject information
@app.callback(
    Output('r-subject-information', 'children'),
    Input('r-subject-dropdown', 'value'),
    Input('r-subject-graph', 'hoverData'),
)
def r_update_timeline_information(selected_subject, hover_data):
    if hover_data is not None:
        text = hover_data['points'][0]['hovertext']
    else:
        text = None
    df, subject, name = rectorfigures.get_variables(selected_subject)
    total = df['count'].sum()
    fraction = df.loc[df[subject] == text, 'count'].sum()
    percentage = round(fraction / total * 100,2)
    return html.Div(id='r-subject-hover-info', children=[
        html.Table(id='r-subject-table', children=[
            html.Tr(children=[
                html.Td('Subject'),
                html.Td(selected_subject),
            ]),
            html.Tr(children=[
                html.Td(str(name) + ' amount'),
                html.Td(df[subject].nunique()),
            ]),
            html.Tr(children=[
                html.Td('Total rectors'),
                html.Td(total),
            ]),
            html.Tr(children=[
                html.Td('Average rectors per year'),
                html.Td(html.Td(round(df['count'].mean(),0))),
            ]),
            html.Tr(children=[
                html.Td('Year with most rectors'),
                html.Td(df.loc[df['count'].max(), subject]),
            ]),
            html.Tr(children=[
                html.Td('Year with least rectors'),
                html.Td(df.loc[df['count'].min(), subject]),
            ]),
        ]),
        html.Br(),
        html.Table(id='r-chosen-subject-table', children=[
            html.Tr(children=[
                html.Td('Year'),
                html.Td(text),
            ]),
            html.Tr(children=[
                html.Td('Rectors'),
                html.Td(fraction),
            ]),
            html.Tr(children=[
                html.Td('Percentage of total rectors'),
                html.Td(percentage),
            ]),
        ]),
        html.Br(),
        html.Div(id='r-century-table'),
    ])


# Subject information table
@app.callback(
    Output('r-century-table', 'children'),
    Input('r-subject-dropdown', 'value'),
)
def r_update_timeline_table(selected_subject):
    df, subject, name = rectorfigures.get_variables(selected_subject)
    table_df = rectorfigures.create_century_table(df, name)
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
        id='r-subject-information-table'
    )


# Individual information callbacks
# Individual table
@app.callback(
    Output('r-individual-search-results-number', 'children'),
    Output('r-individual-search-text', 'children'),
    Output('r-individual-table-container', 'children'),
    Input('r-search-individual', 'n_clicks'),
    Input('r-search-name', 'value'),
    Input('r-search-option', 'value'),
    Input('term-min-input', 'value'),
    Input('term-max-input', 'value'),
    Input('r-include-missing-dates', 'value')
)
def update_student_table(search_button, selected_name, search_option, min_term, max_term, include_missing):
    df = data.recmag_df[['Period_start', 'Period_end', 'Name', 'Picture_saved', 'Term/Details']]
    text = 'rectors were found'
    search_results_number = 0
    if ctx.triggered_id == 'r-search-individual':
        filtered_df = df
        if selected_name is not None and selected_name != '':
            words = selected_name.split(' ')
            temp_total_df = pd.DataFrame()
            for word in words:
                if search_option == 'Contains':
                    temp_df = df[df['Name'].str.contains(word)]
                    if len(temp_df) > 0:
                        temp_total_df = pd.concat((temp_total_df, temp_df), axis=0).drop_duplicates()
                elif search_option == 'Equals':
                    temp_df = df.loc[df['Name'] == word]
                    if len(temp_df) > 0:
                        temp_total_df = pd.concat((temp_total_df, temp_df), axis=0).drop_duplicates()
            if len(temp_total_df) > 0:
                filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            else:
                filtered_df = pd.DataFrame(
                    columns=['Period_start', 'Period_end', 'Name', 'Picture_saved', 'Term/Details'])
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Name'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        if min_term is not None and max_term is not None:
            filtered_df = filtered_df.loc[filtered_df['Period_start'] <= int(max_term)]
            filtered_df = filtered_df[filtered_df['Period_start'] >= int(min_term)]
            if include_missing == 'Yes':
                temp_missing_df = df.loc[df['Period_start'].isnull()]
                if len(temp_missing_df) > 0:
                    filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0).drop_duplicates()
        filtered_df = filtered_df.rename(
            columns={'Period_start': 'Period start', 'Period_end': 'Period end', 'Picture_saved': 'Picture'})
        search_results_number = len(filtered_df)
        return search_results_number, text, dash_table.DataTable(
            data=filtered_df.to_dict('records'),
            columns=[{'id': i, 'name': i, 'hideable': 'last'} for i in filtered_df.columns],
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable='single',
            row_selectable='multi',
            selected_columns=[],
            selected_rows=[],
            page_size=100,
            fixed_rows={'headers': True},
            style_cell={
                'width': '7%',
                'textOverflow': 'ellipsis',
                'overflow': 'hidden'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Period start'},
                 'width': '20%'},
                {'if': {'column_id': 'Period end'},
                 'width': '20%'},
                {'if': {'column_id': 'Name'},
                 'width': '20%'},
                {'if': {'column_id': 'Picture'},
                 'width': '20%'},
                {'if': {'column_id': 'Term/Details'},
                 'width': '20%'},
            ],
            style_header={'backgroundColor': '#001158', 'color': 'white'},
            style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'white', 'color': 'black'},
            virtualization=True,
#           export_format='xlsx', tijdelijk uitgeschakeld
#           export_headers='display',
            merge_duplicate_headers=True,
            id='r-individual-table'
        )
    # else: return None, None, None


# Chosen person information
@app.callback(
    Output('r-chosen-individual-information', 'children'),
    Input('r-individual-table', "derived_virtual_data"),
    Input('r-individual-table', "derived_virtual_selected_rows"),
    Input({'type': 'r-person-table', 'index': ALL}, 'id'),
    State('r-chosen-individual-information', 'children'),
)
def create_individual_information(rows, selected_rows, value, children):
    if rows is None:
        persons = 'No person selected'
    else:
        persons = pd.DataFrame(rows)
    in_list = []
    for v in value:
        if v['index'] not in selected_rows:
            counter = 0
            for child in children:
                if v['index'] == child['props']['id']['index']:
                    children.remove(child)
                counter += 1
        else:
            in_list.append(v['index'])
    for number in selected_rows:
        if number not in in_list:
            person = persons.iloc[number].to_frame().T
            new_person = html.Div(id={'type': 'r-person-table', 'index': number}, className='bigblock',
                                  children=[
                                      html.Table(className='block',
                                                 style={'border': '1px solid black', 'border-collapse': 'collapse'},
                                                 children=[
                                                     html.Tr(children=[
                                                         html.Td('Period start:'),
                                                         html.Td(person.get('Period start')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Period end:'),
                                                         html.Td(person.get('Period end')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Name:'),
                                                         html.Td(person.get('Name')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Picture:'),
                                                         html.Td(person.get('Picture')),
                                                     ]),
                                                     html.Tr(children=[
                                                         html.Td('Royal title:'),
                                                         html.Td(person.get('Terms/Details')),
                                                     ]),
                                                 ]),
                                  ])
            children.append(new_person)
    return children


# term input sync
@app.callback(
    Output('term-min-input', 'value'),
    Output('term-max-input', 'value'),
    Input('term-min-input', 'value'),
    Input('term-max-input', 'value'),
)
def synchronise_dates(min_year, max_year):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == 'term-min-input' and min_year >= max_year:
        if max_year < data.rector_years['year'].max():
            max_year = min_year + 1
        else:
            min_year -= 1
    elif trigger_id == 'term-max-input' and max_year <= min_year:
        if min_year > data.rector_years['year'].min():
            min_year = max_year - 1
        else:
            max_year += 1
    return min_year, max_year

################################################################################################ LOCAL
#if __name__ == '__main__':
#    app.run_server(port=8050, debug=False)
#
################################################################################################ SERVER
if __name__ == '__main__':
    app.run_server(debug=False)
#
################################################################################################# END