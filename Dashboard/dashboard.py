#Creating dataframe
import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, ctx, State, dash_table
from datetime import date
import data
import figures


#Configurate dash application
app = Dash(__name__)
app.config.suppress_callback_exceptions=True

app.layout = html.Div([
    html.H1('The history of Leiden and Leiden University', id='page_title'),
    dcc.Tabs(id='tab_bar', value='tab-2', className='header_tab_bar', children=[
        dcc.Tab(label='Professors', value='tab-1', className='child_tab', selected_className='child_tab_selected'),
        dcc.Tab(label='Students', value='tab-2', className='child_tab', selected_className='child_tab_selected'),
        dcc.Tab(label='Rectores Magnifici', value='tab-3', className='child_tab', selected_className='child_tab_selected'),
    ]),
    html.Div(id='page_content'),
])

profs_content = html.Div(id='p_content', className='parent_content', children=[
    html.Div(id='p_info', className='info', children=[
        html.H2('Information'),
        html.P('Professors'),
    ]),
    html.Div(id='p_timeline', className='left_container', children=[
        html.H2('Timeline'),
    ]),
    html.Div(id='p_var_graph', className='var_graph', children=[
        html.H2('Characteristic graph'),
    ]),
    html.Div(id='p_individual', className='individual', children=[
        html.H2('Individual chart'),
    ]),
    html.Div(id='p_ind_info', className='ind_info', children=[
        html.H2('Individual information'),
        html.H3('Information'),
        html.Table(id='ind_table'),
    ]),
])

students_content = html.Div(id='s_content', className='parent_content', children=[
    html.Div(id='s_info', className='container', children=[
        html.H2('Information'),
        html.P('Students'),
    ]),

    html.Div(id='s_timeline', className='container', children=[
        html.Div(id='s_timeline_header', className='page_header', children=[
            html.H1('Timeline')
        ]),
        html.Div(id='year-century-dropdown-container', className='left_container'),
        html.Div(id='s_inputs', className='right_container ', children=[
            html.H3('Graph settings:'),
            html.P('Select Subject:'),
            dcc.Dropdown(['Number of enrollments', 'Origin countries', 'Origin cities', 'Origin regions', 'Enrollment ages',
                         'Enrollment faculties', 'Royal status', 'Student jobs', 'Student religion'],
                         'Number of enrollments', placeholder='Choose a subject', clearable=False,
                         style={'background-color':'rgb(0,0,80)', 'color':'black', 'margin':'1% 1% 1% 1%'},
                         id='year-century-subject-dropdown', className='dropdown'),
            html.P('Select hovermode:'),
            dcc.RadioItems(
                inline=True,
                options=['x', 'x unified', 'closest'],
                value='closest',
                id='year-hover'
            ),
            html.P('Select year range:'),
            html.Div(id='year-slider-container'),
            html.P('Select century range:'),
            dcc.RangeSlider(
                data.year_df['century'].min(),
                data.year_df['century'].max(),
                1,
                value=[data.year_df['century'].min(), data.year_df['century'].min()],
                marks={str(cent): str(cent) for cent in data.year_df['century']},
                id='year-century-slider'
            ),
            html.P('Select graph type:'),
            dcc.Dropdown(['Line graph', 'Scatter graph', 'Bar graph'], 'Scatter graph', placeholder='Choose a graph style',
                         clearable=False, style={'font-color':'rgb(255,255,255)', 'background-color':'rgb(0,0,80)',
                                                 'color':'black', 'margin':'1% 1% 1% 1%'}, id='year-century-dropdown'),
            html.P('Select age range:'),
            dcc.RangeSlider(
                    data.age_df['age'].min(),
                    90,
                    10,
                    value=[data.age_df['age'].min(), 90],
                    id='subject-slider'
            ),
        ]),
        html.Div(id='century-dropdown-container', className='left_container'),
        html.Div(id='timeline-information', className='right_container ', children=[
            html.H3('Information:'),
            html.Div(id='timeline-information'),
        ]),
    ]),

    html.Div(id='s_subject_info', className='container', children=[
        html.Div(id='s_subject_header', className='page_header', children=[
            html.H1('Subject information')
        ]),
        html.Div(id='subject-container', className='left_container', children=[
            html.Div(id='subject-dropdown-container'),
            html.H3('Subject information:'),
            html.Div(id='subject-table-container'),
        ]),
        html.Div(id='subject-information-container', className='right_container ', children=[
            dcc.Dropdown(['Number of enrollments', 'Origin countries', 'Origin cities', 'Origin regions',
                          'Enrollment ages', 'Enrollment faculties', 'Royal status', 'Student jobs', 'Student religion']
                         , 'Number of enrollments', placeholder='Choose a subject', clearable=False,
                         style={'background-color':'rgb(0,0,80)', 'color':'black', 'margin':'1% 1% 1% 1%'},
                         id='subject-dropdown'),
            html.Div(id='subject-information'),
        ]),
    ]),

    html.Div(id='s_geo', className='container', children=[
        html.Div(id='s_geo_header', className='page_header', children=[
            html.H1('Geographical information')
        ]),
        html.Div(id='geo-map-container', className='left_container', children=[
            html.Div(id='map-container'),
            html.P('Select year range:'),
            html.P('Lowest year', className='inline'),
            dcc.Input(
                id='geo-min-input', className='inline',
                type='number',
                min=data.year_df['year'].min(),
                max=data.year_df['year'].max() - 1,
                value=data.year_df['year'].min(),
                style={'background-color':'rgb(0,0,80)', 'color':'white', 'margin':'1%'},
            ),
            html.P('Highest year', className='inline'),
            dcc.Input(
                id='geo-max-input', className='inline',
                type='number',
                min=data.year_df['year'].min() + 1,
                max=data.year_df['year'].max(),
                value=data.year_df['year'].max(),
                style={'background-color':'rgb(0,0,80)', 'color':'white', 'margin':'1%'},
            ),
        ]),
        html.Div(id='map-info', className='right_container', children=[
            html.H3('Country information'),
            html.Div(id='map-table-container'),
        ]),
    ]),

    html.Div(id='s_individual', className='container', children=[
        html.Div(id='s_student_header', className='page_header', children=[
            html.H1('Student information')
        ]),
        html.Div(id='individual-information', className='left_container', children=[
            html.H3('Student information:'),
            html.Div(id='individual-table-container'),
            html.Div(id='individual-info'),
            html.Div(id='selected-individual-table-container'),
        ]),
        html.Div(id='i_inputs', className='right_container ', children=[
            html.H3('Search settings:'),
            html.P('Search for a name:'),
            dcc.Input(
                id='search-name',
                type='text',
                placeholder='Search name',
                style={'background-color':'rgb(0,0,80)', 'color':'white', 'margin':'1%'},
            ),
            dcc.RadioItems(
                inline=True,
                options=['contains', 'equals'],
                value='contains',
                id='search-option'
            ),
            html.P('Select enrollment year range'),
            dcc.DatePickerRange(
                min_date_allowed=date(int(data.individual_df['Enrollment year'].min()), 1, 1),
                max_date_allowed=date(int(data.individual_df['Enrollment year'].max()), 12, 31),
                initial_visible_month=date(int(data.individual_df['Enrollment year'].min()), 1, 1),
                start_date=date(int(data.individual_df['Enrollment year'].min()), 1, 1),
                end_date=date(int(data.individual_df['Enrollment year'].max()), 12, 31),
                style={'background-color': 'rgb(0,0,80)', 'color': 'white', 'fontSize': '10', 'margin': '1%'},
                id='year-range'
            ),
            html.Div(id='output-year-range'),
            html.P('Select birthyear range:'),
            dcc.DatePickerRange(
                min_date_allowed=date(int(data.individual_df['Birth year'].min()), 1, 1),
                max_date_allowed=date(int(data.individual_df['Birth year'].max()), 12, 31),
                initial_visible_month=date(int(data.individual_df['Birth year'].min()), 1, 1),
                start_date=date(int(data.individual_df['Birth year'].min()), 1, 1),
                end_date=date(int(data.individual_df['Birth year'].max()), 12, 31),
                style={'background-color': 'rgb(0,0,80)', 'color': 'white', 'fontSize': '10', 'margin': '1%'},
                id='birthyear-range'
            ),
            html.Div(id='output-birthyear-range'),
            html.P('Select enrollment age:'),
            dcc.RangeSlider(
                    int(data.individual_df['Enrollment age'].min()),
                    90,
                    10,
                    value=[int(data.individual_df['Enrollment age'].min()), 90],
                    id='individual-age-slider'
            ),
            html.P('Select cities:'),
            dcc.Dropdown(figures.get_unique_values('City'), placeholder='Choose a city', clearable=False,
                         style={'background-color':'rgb(0,0,80)', 'color':'black', 'margin':'1% 1% 1% 1%'},
                         multi=True, id='individual-city-dropdown', className='dropdown'),
            html.P('Select countries:'),
            dcc.Dropdown(data.individual_df['Country'].unique(), placeholder='Choose a country', clearable=False,
                         style={'background-color': 'rgb(0,0,80)', 'color': 'black', 'margin': '1% 1% 1% 1%'},
                         multi=True, id='individual-country-dropdown', className='dropdown'),
            html.P('Select region:'),
            dcc.Dropdown(data.individual_df['Region'].unique(), placeholder='Choose a region', clearable=False,
                         style={'background-color': 'rgb(0,0,80)', 'color': 'black', 'margin': '1% 1% 1% 1%'},
                         multi=True, id='individual-region-dropdown', className='dropdown'),
            html.P('Select faculty:'),
            dcc.Dropdown(data.individual_df['Faculty'].unique(), placeholder='Choose a faculty', clearable=False,
                         style={'background-color': 'rgb(0,0,80)', 'color': 'black', 'margin': '1% 1% 1% 1%'},
                         multi=True, id='individual-faculty-dropdown', className='dropdown'),
            html.P('Select royal title:'),
            dcc.Dropdown(figures.remove_nan('Royal title'), placeholder='Choose a royal title', clearable=False,
                         style={'background-color': 'rgb(0,0,80)', 'color': 'black', 'margin': '1% 1% 1% 1%'},
                         multi=True, id='individual-royal-dropdown', className='dropdown'),
            html.P('Select job:'),
            dcc.Dropdown(figures.remove_nan('Job'), placeholder='Choose a job', clearable=False,
                         style={'background-color': 'rgb(0,0,80)', 'color': 'black', 'margin': '1% 1% 1% 1%'},
                         multi=True, id='individual-job-dropdown', className='dropdown'),
            html.P('Select religion:'),
            dcc.Dropdown(figures.remove_nan('Religion'), placeholder='Choose a religion', clearable=False,
                         style={'background-color': 'rgb(0,0,80)', 'color': 'black', 'margin': '1% 1% 1% 1%'},
                         multi=True, id='individual-religion-dropdown', className='dropdown'),
        ]),
    ]),
])

recmag_content = html.Div(id='rm_content', className='parent_content', children=[
    html.Div(id='rm_info', className='info', children=[
        html.H2('Information'),
        html.P('Rectores Magnifici'),
    ]),
    html.Div(id='rm_timeline', className='left_container', children=[
        html.H2('Timeline'),
    ]),
    html.Div(id='rm_var_graph', className='var_graph', children=[
        html.H2('Characteristic graph'),
    ]),
    html.Div(id='rm_individual', className='individual', children=[
        html.H2('Individual chart'),
    ]),
    html.Div(id='rm_ind_info', className='ind_info', children=[
        html.H2('Individual information'),
        html.H3('Information'),
        html.Table(id='ind_table'),
    ]),
])

# Index callbacks
@app.callback(
    Output('page_content', 'children'),
    Input('tab_bar', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return profs_content
    if tab == 'tab-2':
        return students_content
    if tab == 'tab-3':
        return recmag_content
    else:
        return profs_content


# Students callbacks
# Year slider
@app.callback(
    Output('year-slider-container', 'children'),
    Input('year-century-slider', 'value'),
)
def update_year_slider(century):
    current_century = data.year_df[(data.year_df['century'] <= century[-1])]
    years = []
    for y in current_century['year'][0::5]:
        years.append(y)
        years.append(current_century['year'].max())
    return (dcc.RangeSlider(
        current_century['year'].min(),
        current_century['year'].max(),
        5,
        value=[current_century['year'].min(), current_century['year'].max()],
        marks={str(year): str(year) for year in years},
        id='year-slider'
        ))


# year-century graph
@app.callback(
    Output('year-century-dropdown-container', 'children'),
    Input('year-century-subject-dropdown', 'value'),
    Input('year-century-slider', 'value'),
    Input('year-slider', 'value'),
    Input('subject-slider', 'value'),
    Input('year-century-dropdown', 'value'),
    Input('year-hover', 'value')
)
def update_year_century_output(selected_subject, selected_century, selected_year, selected_age, selected_dropdown, selected_hover):
    return dcc.Graph(figure=figures.create_year_cent_figure(selected_subject, selected_century, selected_year,
                                                            selected_age, selected_dropdown, selected_hover),
                                                            id='year-century-graph')


# century-graph
@app.callback(
    Output('century-dropdown-container', 'children'),
    Input('year-century-subject-dropdown', 'value'),
    Input('year-century-slider', 'value'),
)
def update_century_output(selected_subject, selected_century):
    return dcc.Graph(figure=figures.create_cent_figure(selected_subject, selected_century), id='century-graph')


# Timeline information
@app.callback(
    Output('timeline-information', 'children'),
    Input('year-century-subject-dropdown', 'value'),
    Input('year-century-graph', 'hoverData'),
    Input('century-graph', 'value')
)
def update_timeline_information(selected_subject, hover_data, century_data):
    text = hover_data['points'][0]['hovertext']
    y = hover_data['points'][0]['x']
    year = int(y)
    df, subject, name = figures.get_variables(selected_subject)
    century = df.loc[df['year'] == year, 'century'].values[0]
    enrollments = df.loc[df['year'] == year, 'count'].values[0]
    last_year = year - 1
    last_year_enrollments = df.loc[df['year'] == last_year, 'count'].values[0]
    growth = enrollments - last_year_enrollments
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
                html.Td(df['count'].mean().round(0)),
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
                html.Td(df['count'].mean().round(0)),
            ]),
        ]),


# subject-graph
@app.callback(
    Output('subject-dropdown-container', 'children'),
    Input('subject-dropdown', 'value')
)
def update_subject_output(selected_subject):
    return dcc.Graph(figure=figures.create_subject_info_graph(selected_subject), id='subject-graph')


# Subject table
@app.callback(
    Output('subject-table-container', 'children'),
    Input('subject-dropdown', 'value'),
)
def update_timeline_table(selected_subject):
    df, subject, name = figures.get_variables(selected_subject)
    df = df.rename(columns={subject: name, 'year': 'Year', 'count': 'Enrollments', 'century': 'Century'})
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': i, 'name': i} for i in df.columns],
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
        style_header={'backgroundColor': 'white', 'color': 'black'},
        style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'rgb(0,0,90)', 'color': 'white'},
        id='subject-table'
    )


# Subject information
@app.callback(
    Output('subject-information', 'children'),
    Input('subject-dropdown', 'value'),
    Input('subject-graph', 'hoverData'),
)
def update_timeline_information(selected_subject, hover_data):
    text = hover_data['points'][0]['hovertext']
    df, subject, name = figures.get_variables(selected_subject)
    total = df['count'].sum()
    fraction = df.loc[df[subject] == text, 'count'].sum()
    percentage = (fraction / total * 100).round(2)
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
                    html.Td(html.Td(df['count'].mean().round(0))),
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
            html.Div(id='century-table'),
            html.Br(),
            html.Table(id='chosen-subject-table', children=[
                html.Tr(children=[
                    html.Td(name),
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
            # figures.create_subject_table(df, name, subject, text)
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
                    html.Td('Average enrollments per ' + str(subject)),
                    html.Td(html.Td(df['count'].mean().round(0))),
                ]),
                html.Tr(children=[
                    html.Td(str(name) + ' with most enrollments'),
                    html.Td(df.loc[df['count'] == df['count'].max(), subject].unique()),
                ]),
                html.Tr(children=[
                    html.Td(str(name) + ' with least enrollments'),
                    html.Td(df.loc[df['count'] == df['count'].min(), subject].unique()),
                ]),
            ]),
            html.Br(),
            html.Div(id='century-table'),
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
            #figures.create_subject_table(df, name, subject, text)
        ])


# Subject information table
@app.callback(
    Output('century-table', 'children'),
    Input('subject-dropdown', 'value'),
)
def update_timeline_table(selected_subject):
    df, subject, name = figures.get_variables(selected_subject)
    table_df = figures.create_century_table(df, name)
    return dash_table.DataTable(
        data=table_df.to_dict('records'),
        columns=[{'id': i, 'name': i} for i in table_df.columns],
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_size=100,
        fixed_rows={'headers': True},
        style_cell={
            'width': '{}%'.format(len(table_df.columns)),
            'textOverflow': 'ellipsis',
            'overflow': 'hidden'
        },
        style_table={'overflowY': 'auto', 'overflowX': 'auto'},
        style_header={'backgroundColor': 'white', 'color': 'black'},
        style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'rgb(0,0,90)', 'color': 'white'},
        id='subject-information-table'
    )


# geo map
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


@app.callback(
    Output('map-container', 'children'),
    Output('map-table-container', 'children'),
    Input('geo-min-input', 'value'),
    Input('geo-max-input', 'value'),
)
def create_map(min_year, max_year):
    figure, geo_data = figures.create_country_map(min_year, max_year)
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
        style_cell_conditional=[
            #{'if': {'column_id': 'Statistic'},
             #'width': '80%'},
            {'if': {'column_id': 'Enrollments'},
             'width': '10%'},
            {'if': {'column_id': 'Century'},
             'width': '10%'},
            ],
        style_table={'overflowY': 'auto', 'overflowX': 'auto'},
        style_header={'backgroundColor': 'white', 'color': 'black'},
        style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'rgb(0,0,90)', 'color': 'white'},
        id='geo-map-table'
    )
    return dcc.Graph(figure=figure, id='geo-map'), geo_table

# Individual table
@app.callback(
    Output('individual-table-container', 'children'),
    Input('search-name', 'value'),
    Input('search-option', 'value'),
    Input('year-range', 'value'),
    Input('birthyear-range', 'value'),
    Input('individual-age-slider', 'value'),
    Input('individual-city-dropdown', 'value'),
    Input('individual-country-dropdown', 'value'),
    Input('individual-region-dropdown', 'value'),
    Input('individual-faculty-dropdown', 'value'),
    Input('individual-royal-dropdown', 'value'),
    Input('individual-job-dropdown', 'value'),
    Input('individual-religion-dropdown', 'value'),
)
def update_student_table(selected_name, search_option, selected_year, selected_birthyear, selected_age, selected_city,
                         selected_country, selected_region, selected_faculty, selected_royal, selected_job,
                         selected_religion):
    df = data.individual_df[['First name', 'Last name', 'Enrollment year', 'City', 'Country', 'Region', 'Enrollment age'
                             , 'Birth year', 'Faculty', 'Royal title', 'Job', 'Religion', 'Enrollments']]
    filtered_df = pd.DataFrame()
    if selected_name is not None:
        words = selected_name.split(' ')
        for word in words:
            if search_option == 'contains':
                temp_df = df[df['First name'].str.contains(word)]
                filtered_df = pd.concat((filtered_df, temp_df), axis=0)
                temp_df = df[df['Last name'].str.contains(word)]
                filtered_df = pd.concat((filtered_df, temp_df), axis=0)
            elif search_option == 'equals':
                temp_df = df.loc[df['First name'] == word]
                filtered_df = pd.concat((filtered_df, temp_df), axis=0)
                temp_df = df.loc[df['Last name'] == word]
                filtered_df = pd.concat((filtered_df, temp_df), axis=0)
    if selected_year is not None:
        print(selected_year)
    if selected_birthyear is not None:
        print(selected_birthyear)
    if selected_age is not None:
        filtered_df = filtered_df[filtered_df['Enrollment age'] <= int(selected_age[1])]
        filtered_df = filtered_df[filtered_df['Enrollment age'] >= int(selected_age[0])]
    if selected_city is not None:
        for c in selected_city:
            temp_df = df.loc[df['City'] == c]
            filtered_df = pd.concat((filtered_df, temp_df), axis=0)
    if selected_country is not None:
        for c in selected_country:
            temp_df = df.loc[df['Country'] == c]
            filtered_df = pd.concat((filtered_df, temp_df), axis=0)
    if selected_region is not None:
        for c in selected_region:
            temp_df = df.loc[df['Region'] == c]
            filtered_df = pd.concat((filtered_df, temp_df), axis=0)
    if selected_faculty is not None:
        for c in selected_faculty:
            temp_df = df.loc[df['Faculty'] == c]
            filtered_df = pd.concat((filtered_df, temp_df), axis=0)
    if selected_royal is not None:
        for c in selected_royal:
            temp_df = df.loc[df['Royal title'] == c]
            filtered_df = pd.concat((filtered_df, temp_df), axis=0)
    if selected_job is not None:
        for c in selected_job:
            temp_df = df.loc[df['Job'] == c]
            filtered_df = pd.concat((filtered_df, temp_df), axis=0)
    if selected_religion is not None:
        for c in selected_religion:
            temp_df = df.loc[df['Religion'] == c]
            filtered_df = pd.concat((filtered_df, temp_df), axis=0)
    return dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        columns=[{'id': i, 'name': i} for i in filtered_df.columns],
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_size=100,
        fixed_rows={'headers': True},
        style_cell={
            'width': '{}%'.format(len(filtered_df.columns)),
            'textOverflow': 'ellipsis',
            'overflow': 'hidden'
        },
        style_table={'overflowY': 'auto', 'overflowX': 'auto'},
        style_header={'backgroundColor': 'white', 'color': 'black'},
        style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'rgb(0,0,90)', 'color': 'white'},
        id='individual-table'
    )


@app.callback(
    Output('output-year-range', 'children'),
    Input('year-range', 'start_date'),
    Input('year-range', 'end_date'))
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix


@app.callback(
    Output('output-birthyear-range', 'children'),
    Input('birthyear-range', 'start_date'),
    Input('birthyear-range', 'end_date'))
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix


# Individual hover table
@app.callback(
    Output('selected-individual-table-container', 'children'),
    Input('individual-table', 'hoverData'),
)
def update_selected_student_table(hover_data):
    print(hover_data)
    return


if __name__ == '__main__':
    app.run_server(debug=True)