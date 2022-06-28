from dash import Dash, dcc, html, Input, Output, ctx, dash_table
import pandas as pd
import data
import figures
import professorvisuals
import rectorvisuals
import studentvisuals

# Configurate dash application

app = Dash(__name__)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1('The history of Leiden and Leiden University', id='page_title'),
    dcc.Tabs(id='tab_bar', value='tab-2', className='header_tab_bar', children=[
        dcc.Tab(label='Home', value='tab-0', className='child_tab', selected_className='child_tab_selected'),
        dcc.Tab(label='Professors', value='tab-1', className='child_tab', selected_className='child_tab_selected'),
        dcc.Tab(label='Students', value='tab-2', className='child_tab', selected_className='child_tab_selected'),
        dcc.Tab(label='Rectores Magnifici', value='tab-3', className='child_tab',
                selected_className='child_tab_selected'),
    ]),
    html.Div(id='page_content'),
])

home_content = html.Div(id='h_content', className='parent_content', children=[
    html.Div(id='h_info', className='container', children=[
        html.H2('Welcome'),
        html.P('This dashboard is created for the Linking University, City and Diversity project by the university of '
               'Leiden as part of a bachelor project. To get started, select one of the three options in the navigation'
               ' bar at the top of the page. This brings you to the corresponding page that gives detailed information '
               'about the chosen subject.')
    ]),
])

profs_content = html.Div(id='p_content', className='parent_content', children=[
    html.H2('Information'),
    html.P('This pages shows the information about professors previously working at the university of Leiden.'
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
        html.P('This pages shows the information about student enrollments from the period 1575 to 1812. Choose one of '
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
    html.P('This pages shows the information about all the rectores magnifici the university of Leiden has had.'
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
    else:
        return home_content


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
        return professorvisuals.timeline


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
        return studentvisuals.timeline


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
        return rectorvisuals.timeline


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
)
def update_year_century_output(selected_subject, selected_century, selected_year, selected_age, selected_dropdown):
    return dcc.Graph(figure=figures.create_year_cent_figure(selected_subject, selected_century, selected_year,
                                                            selected_age, selected_dropdown),
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
)
def update_timeline_information(selected_subject, hover_data):
    if hover_data is not None:
        text = hover_data['points'][0]['hovertext']
        y = hover_data['points'][0]['x']
        year = int(y)
    else:
        text = None
        year = data.year_df['year'].min()
    df, subject, name = figures.get_variables(selected_subject)
    century = df.loc[df['year'] == year, 'century'].values[0]
    enrollments = df.loc[df['year'] == year, 'count'].values[0]
    last_year = year - 1
    if last_year >= df['year'].min():
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


# Subject information callbacks
# Subject-graph
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
        style_header={'backgroundColor': '#001158', 'color': 'white'},
        style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'white', 'color': 'black'},
        virtualization=True,
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
                    html.Td(html.Td(df['count'].mean().round(0))),
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
    df, subject, name = figures.get_variables(selected_subject)
    table_df = figures.create_century_table(df, name)
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
        figure, geo_data = figures.create_country_map(min_year, max_year)
    elif map_choice == 'Line map':
        figure, geo_data = figures.create_country_line_map(min_year, max_year)
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
    Output('individual-table-container', 'children'),
    Output('individual-dropdown', 'children'),
    Output('compare-dropdown', 'children'),
    Input('search-name', 'value'),
    Input('search-option', 'value'),
    Input('enrollment-min-input', 'value'),
    Input('enrollment-max-input', 'value'),
    Input('birthyear-min-input', 'value'),
    Input('birthyear-max-input', 'value'),
    Input('individual-age-slider', 'value'),
    Input('individual-city-dropdown', 'value'),
    Input('individual-country-dropdown', 'value'),
    Input('individual-region-dropdown', 'value'),
    Input('individual-faculty-dropdown', 'value'),
    Input('individual-royal-dropdown', 'value'),
    Input('individual-job-dropdown', 'value'),
    Input('individual-religion-dropdown', 'value'),
)
def update_student_table(selected_name, search_option, min_enrol, max_enrol, min_birth, max_birth,
                         selected_age, selected_city, selected_country, selected_region, selected_faculty,
                         selected_royal, selected_job, selected_religion):
    df = data.individual_df[['First name', 'Last name', 'Enrollment year', 'City', 'Country', 'Region', 'Enrollment age'
        , 'Birth year', 'Faculty', 'Royal title', 'Job', 'Religion', 'Enrollments']]
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
                                                'Job', 'Religion', 'Enrollments'])
    if min_enrol is not None and max_enrol is not None:
        filtered_df = filtered_df.loc[filtered_df['Enrollment year'] <= int(max_enrol)]
        filtered_df = filtered_df[filtered_df['Enrollment year'] >= int(min_enrol)]
    if min_birth is not None and max_enrol is not None:
        filtered_df = filtered_df.loc[filtered_df['Birth year'] <= int(max_birth)]
        filtered_df = filtered_df[filtered_df['Birth year'] >= int(min_birth)]
    if selected_age is not None:
        filtered_df = filtered_df.loc[filtered_df['Enrollment age'] <= int(selected_age[1])]
        filtered_df = filtered_df[filtered_df['Enrollment age'] >= int(selected_age[0])]
    if selected_city is not None:
        temp_total_df = pd.DataFrame()
        for c in selected_city:
            temp_df = df.loc[df['City'] == c]
            temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
        filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
    if selected_country is not None:
        temp_total_df = pd.DataFrame()
        for c in selected_country:
            temp_df = df.loc[df['Country'] == c]
            temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
        filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
    if selected_region is not None:
        temp_total_df = pd.DataFrame()
        for c in selected_region:
            temp_df = df.loc[df['Region'] == c]
            temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
        filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
    if selected_faculty is not None:
        temp_total_df = pd.DataFrame()
        for c in selected_faculty:
            temp_df = df.loc[df['Faculty'] == c]
            temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
        filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
    if selected_royal is not None:
        temp_total_df = pd.DataFrame()
        for c in selected_royal:
            temp_df = df.loc[df['Royal title'] == c]
            temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
        filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
    if selected_job is not None:
        temp_total_df = pd.DataFrame()
        for c in selected_job:
            temp_df = df.loc[df['Job'] == c]
            temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
        filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
    if selected_religion is not None:
        temp_total_df = pd.DataFrame()
        for c in selected_religion:
            temp_df = df.loc[df['Religion'] == c]
            temp_total_df = pd.concat([temp_total_df, temp_df], axis=0).drop_duplicates()
        filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
    filtered_df = filtered_df.rename(columns={'Enrollment year': 'Year', 'Enrollment age': 'Age'})
    chosen_names = []
    first_names = filtered_df['First name'].tolist()
    last_names = filtered_df['Last name'].tolist()
    for f_name, l_name in zip(first_names, last_names):
        chosen_names.append(f_name + ';' + l_name)
    print('hier')
    return dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        columns=[{'id': i, 'name': i} for i in filtered_df.columns],
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
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
             'width': '9%'},
            {'if': {'column_id': 'Faculty'},
             'width': '9%'},
            {'if': {'column_id': 'Royal title'},
             'width': '10%'},
            {'if': {'column_id': 'Job'},
             'width': '5%'},
            {'if': {'column_id': 'Religion'},
             'width': '10%'},
            {'if': {'column_id': 'Enrollments'},
             'width': '10%'},
        ],
        style_header={'backgroundColor': '#001158', 'color': 'white'},
        style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'white', 'color': 'black'},
        virtualization=True,
        id='individual-table'
    ), dcc.Dropdown(chosen_names, placeholder='Choose a person', clearable=False,
                    style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1% 1% 1% 1%'},
                    id='choose-individual-dropdown', className='dropdown'), \
           dcc.Dropdown(chosen_names, placeholder='Choose a person', clearable=False,
                        style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1% 1% 1% 1%'},
                        id='compare-individual-dropdown', className='dropdown')


# Chosen person information
@app.callback(
    Output('chosen-individual-information', 'children'),
    Output('individual-map', 'figure'),
    Input('choose-individual-dropdown', 'value'),
)
def create_individual_information(name):
    if name is not None:
        df = data.individual_df
        name_parts = str(name).split(';')
        temp_df = df.loc[df['First name'] == name_parts[0]]
        person = temp_df.loc[temp_df['Last name'] == name_parts[1]]
        attributes = ['First name', 'Last name', 'Birth year', 'City', 'Country', 'Region', 'Honor', 'Royal title',
                      'Enrollment day', 'Enrollment month', 'Enrollment year', 'Enrollment age', 'Faculty', 'Job',
                      'Religion', 'Extra', 'Remark', 'Previous enrollment', 'Previous faculty', 'Original faculty']
        attribute_dict = {}
        for attribute in attributes:
            temp = person[attribute].tolist()
            for t in temp:
                if t in attribute_dict:
                    if attribute_dict[attribute] != t:
                        old = attribute_dict[attribute]
                        print(old)
                        new = old + ', ' + t
                        print(new)
                        attribute_dict.update({attribute: new})
                else:
                    attribute_dict[attribute] = t
        return html.Table(id='chosen-individual-table', children=[
            html.Tr(children=[
                html.Td('First name'),
                html.Td(attribute_dict.get('First name')),
            ]),
            html.Tr(children=[
                html.Td('Last name'),
                html.Td(attribute_dict.get('Last name')),
            ]),
            html.Tr(children=[
                html.Td('Birth year'),
                html.Td(attribute_dict.get('Birth year')),
            ]),
            html.Tr(children=[
                html.Td('City'),
                html.Td(attribute_dict.get('City')),
            ]),
            html.Tr(children=[
                html.Td('Country'),
                html.Td(attribute_dict.get('Country')),
            ]),
            html.Tr(children=[
                html.Td('Region'),
                html.Td(attribute_dict.get('Region')),
            ]),
            html.Tr(children=[
                html.Td('Honorary title'),
                html.Td(attribute_dict.get('Honor')),
            ]),
            html.Tr(children=[
                html.Td('Royal title'),
                html.Td(attribute_dict.get('Royal title')),
            ]),
            html.Tr(children=[
                html.Td('Enrollment day'),
                html.Td(attribute_dict.get('Enrollment day')),
            ]),
            html.Tr(children=[
                html.Td('Enrollment month'),
                html.Td(attribute_dict.get('Enrollment month')),
            ]),
            html.Tr(children=[
                html.Td('Enrollment year'),
                html.Td(attribute_dict.get('Enrollment year')),
            ]),
            html.Tr(children=[
                html.Td('Enrollment age'),
                html.Td(attribute_dict.get('Enrollment age')),
            ]),
            html.Tr(children=[
                html.Td('Faculty'),
                html.Td(attribute_dict.get('Faculty')),
            ]),
            html.Tr(children=[
                html.Td('Job'),
                html.Td(attribute_dict.get('Job')),
            ]),
            html.Tr(children=[
                html.Td('Religion'),
                html.Td(attribute_dict.get('Religion')),
            ]),
            html.Tr(children=[
                html.Td('Extra'),
                html.Td(attribute_dict.get('Extra')),
            ]),
            html.Tr(children=[
                html.Td('Remark'),
                html.Td(attribute_dict.get('Remark')),
            ]),
            html.Tr(children=[
                html.Td('Previous enrollment'),
                html.Td(attribute_dict.get('Previous enrollment')),
            ]),
            html.Tr(children=[
                html.Td('Previous faculty'),
                html.Td(attribute_dict.get('Previous faculty')),
            ]),
            html.Tr(children=[
                html.Td('Original faculty'),
                html.Td(attribute_dict.get('Original faculty')),
            ]),
        ]), dcc.Graph(figure=figures.create_map(attribute_dict.get('City'), attribute_dict.get('Country'),
                               attribute_dict.get('Birth year'), attribute_dict.get('Enrollment age')), id='ind-map')
    else:
        return None, None


# Compare person information
@app.callback(
    Output('compare-individual-information', 'children'),
    Output('compare-map', 'figure'),
    Input('compare-individual-dropdown', 'value'),
)
def create_individual_information(name):
    if name is not None:
        df = data.individual_df
        name_parts = str(name).split(';')
        temp_df = df.loc[df['First name'] == name_parts[0]]
        person = temp_df.loc[temp_df['Last name'] == name_parts[1]]
        attributes = ['First name', 'Last name', 'Birth year', 'City', 'Country', 'Region', 'Honor', 'Royal title',
                      'Enrollment day', 'Enrollment month', 'Enrollment year', 'Enrollment age', 'Faculty', 'Job',
                      'Religion', 'Extra', 'Remark', 'Previous enrollment', 'Previous faculty', 'Original faculty']
        attribute_dict = {}
        for attribute in attributes:
            temp = person[attribute].tolist()
            for t in temp:
                if t in attribute_dict:
                    if attribute_dict[attribute] != t:
                        old = attribute_dict[attribute]
                        print(old)
                        new = old + ', ' + t
                        print(new)
                        attribute_dict.update({attribute: new})
                else:
                    attribute_dict[attribute] = t
        return html.Table(id='compare-individual-table', children=[
            html.Tr(children=[
                html.Td('First name'),
                html.Td(attribute_dict.get('First name')),
            ]),
            html.Tr(children=[
                html.Td('Last name'),
                html.Td(attribute_dict.get('Last name')),
            ]),
            html.Tr(children=[
                html.Td('Birth year'),
                html.Td(attribute_dict.get('Birth year')),
            ]),
            html.Tr(children=[
                html.Td('City'),
                html.Td(attribute_dict.get('City')),
            ]),
            html.Tr(children=[
                html.Td('Country'),
                html.Td(attribute_dict.get('Country')),
            ]),
            html.Tr(children=[
                html.Td('Region'),
                html.Td(attribute_dict.get('Region')),
            ]),
            html.Tr(children=[
                html.Td('Honorary title'),
                html.Td(attribute_dict.get('Honor')),
            ]),
            html.Tr(children=[
                html.Td('Royal title'),
                html.Td(attribute_dict.get('Royal title')),
            ]),
            html.Tr(children=[
                html.Td('Enrollment day'),
                html.Td(attribute_dict.get('Enrollment day')),
            ]),
            html.Tr(children=[
                html.Td('Enrollment month'),
                html.Td(attribute_dict.get('Enrollment month')),
            ]),
            html.Tr(children=[
                html.Td('Enrollment year'),
                html.Td(attribute_dict.get('Enrollment year')),
            ]),
            html.Tr(children=[
                html.Td('Enrollment age'),
                html.Td(attribute_dict.get('Enrollment age')),
            ]),
            html.Tr(children=[
                html.Td('Faculty'),
                html.Td(attribute_dict.get('Faculty')),
            ]),
            html.Tr(children=[
                html.Td('Job'),
                html.Td(attribute_dict.get('Job')),
            ]),
            html.Tr(children=[
                html.Td('Religion'),
                html.Td(attribute_dict.get('Religion')),
            ]),
            html.Tr(children=[
                html.Td('Extra'),
                html.Td(attribute_dict.get('Extra')),
            ]),
            html.Tr(children=[
                html.Td('Remark'),
                html.Td(attribute_dict.get('Remark')),
            ]),
            html.Tr(children=[
                html.Td('Previous enrollment'),
                html.Td(attribute_dict.get('Previous enrollment')),
            ]),
            html.Tr(children=[
                html.Td('Previous faculty'),
                html.Td(attribute_dict.get('Previous faculty')),
            ]),
            html.Tr(children=[
                html.Td('Original faculty'),
                html.Td(attribute_dict.get('Original faculty')),
            ]),
        ]), dcc.Graph(figure=figures.create_map(attribute_dict.get('City'), attribute_dict.get('Country'),
                               attribute_dict.get('Birth year'), attribute_dict.get('Enrollment age')), id='com-map')
    else:
        return None, None


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


if __name__ == '__main__':
    app.run_server(debug=True)
