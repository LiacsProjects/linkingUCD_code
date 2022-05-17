#Creating dataframe
import dash
from dash import Dash, dcc, html, Input, Output, dash_table
from collections import OrderedDict
import data
import figures
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import json

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
        html.Div(id='year-century-dropdown-container', className='left_container'),
        html.Div(id='s_inputs', className='right_container ', children=[
            html.H3('Graph settings:'),
            html.P('Select Subject:'),
            dcc.Dropdown(['Number of enrollments', 'Origin countries', 'Origin cities', 'Origin regions', 'Enrollment ages',
                     'Enrollment faculties', 'Royal status', 'Student jobs', 'Student religion'],
                     'Number of enrollments', placeholder='Choose a subject', clearable=False,
                     style={'background-color':'rgb(0,0,80)', 'color':'black', 'margin':'1% 1% 1% 1%'}, id='year-century-subject-dropdown'),
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
        html.Div(id='subject-container', className='left_container', children=[
            html.Div(id='subject-dropdown-container'),
            dcc.Dropdown(['Number of enrollments', 'Origin countries', 'Origin cities', 'Origin regions',
                          'Enrollment ages', 'Enrollment faculties', 'Royal status', 'Student jobs', 'Student religion']
                         , 'Number of enrollments', placeholder='Choose a subject', clearable=False,
                         style={'background-color':'rgb(0,0,80)', 'color':'black', 'margin':'1% 1% 1% 1%'},
                         id='subject-dropdown'),
        ]),
        html.Div(id='subject-information-container', className='right_container ', children=[
            html.H3('Subject information:'),
            html.Div(id='subject-table-container'),
            html.Div(id='subject-info'),
            html.Div(id='hover-data')
        ]),
    ]),

    html.Div(id='s_geo', className='container', children=[
        dcc.Graph(figure=figures.countrymapfig, id='country_figure', className='left_container'),
        html.Div(id='map-info', className='right_container', children=[
            html.H3('Country information'),
        ]),
    ]),

    html.Div(id='s_individual', className='container', children=[
        html.Div(id='individual-chart', className='left_container', children=[

        ]),
        html.Div(id='individual-information', className='right_container', children=[
            html.H3('Information'),

        ])
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
)
def update_timeline_information(selected_subject, hover_data):
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
                html.Th('Subject:'),
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
                html.Th('Subject:'),
                html.Th(selected_subject),
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
    df.rename(columns={'year': 'Year', 'count': 'Number of enrollments', 'subject': name})
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': i, 'name': i} for i in df.columns],
        page_size=100,
        fixed_rows={'headers': True},
        style_table={'overflowY': 'auto', 'overflowX': 'auto'},
        style_header={'backgroundColor': 'white', 'color': 'black'},
        style_data={'backgroundColor': 'rgb(0,0,90)', 'color': 'white'},
        id='subject-table'
    )


"""
@app.callback(
    Output(),
    Input(),
)
def
"""
if __name__ == '__main__':
    app.run_server(debug=True)