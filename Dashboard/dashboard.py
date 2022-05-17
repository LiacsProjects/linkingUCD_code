#Creating dataframe
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
    dcc.Tabs(id='tab_bar', value='tab-1', className='header_tab_bar', children=[
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
    html.Div(id='p_timeline', className='timeline', children=[
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
    html.Div(id='s_info', className='info', children=[
        html.H2('Information'),
        html.P('Students'),
    ]),
    html.Div(id='s_timeline_info', className='info', children=[
        html.Div(id='s_timeline', className='timeline', children=[
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
            html.Div(id='year-century-dropdown-container'),
            html.Div(id='subject-slider-container'),
            html.P('Select the years to view:'),
            html.Div(id='year-slider-container'),
            html.Div(id='year-info'),
            html.P('Select which centuries to view:'),
            dcc.RangeSlider(
                data.year_df['century'].min(),
                data.year_df['century'].max(),
                1,
                value=[data.year_df['century'].min(), data.year_df['century'].min()],
                marks={str(cent): str(cent) for cent in data.year_df['century']},
                id='year-century-slider'
            ),
            dcc.Dropdown(['Line graph', 'Scatter graph', 'Bar graph'], 'Scatter graph', placeholder='Choose a graph style',
                         clearable=False, style={'font-color':'rgb(255,255,255)', 'background-color':'rgb(0,0,80)',
                                                 'color':'black', 'margin':'1% 1% 1% 1%'}, id='year-century-dropdown'),
        ]),
        html.Div(id='s_var_graph', className='var_graph', children=[
            html.Div(id='century-dropdown-container'),
            html.H3('Information:'),
            html.Div(id='timeline-information'),
            html.Div(id='timeline-table-container'),
        ]),
    ]),
    html.Div(id='s_subject_info', className='subject', children=[
        dcc.Dropdown(['Number of enrollments', 'Origin countries', 'Origin cities', 'Origin regions', 'Enrollment ages',
                     'Enrollment faculties', 'Royal status', 'Student jobs', 'Student religion'],
                     'Number of enrollments', placeholder='Choose a subject', clearable=False,
                     style={'background-color':'rgb(0,0,80)', 'color':'black', 'margin':'1% 1% 1% 1%'}, id='subject-dropdown'),
        html.Div(id='subject-dropdown-container'),
        html.Div(id='subject-info'

                 ),
    ]),
    html.Div(id='s_map1', className='country_map', children=[
        dcc.Graph(figure=figures.countrymapfig, id='country_figure')
    ]),
    html.Div(id='s_individual', className='individual', children=[
        html.H2('Individual chart'),
    ]),
    html.Div(id='s_ind_info', className='ind_info', children=[
        html.H2('Individual information'),
        html.H3('Information'),
        html.Table(id='ind_table'),
    ]),
])

recmag_content = html.Div(id='rm_content', className='parent_content', children=[
    html.Div(id='rm_info', className='info', children=[
        html.H2('Information'),
        html.P('Rectores Magnifici'),
    ]),
    html.Div(id='rm_timeline', className='timeline', children=[
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
# year-century graph
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


@app.callback(
    Output('subject-slider-container', 'children'),
    Input('year-century-subject-dropdown', 'value'),
)
def update_subject_slider(selected_subject):
    if selected_subject == 'Enrollment ages':
        df, subject, name = figures.get_variables(selected_subject)
        return dcc.RangeSlider(
                df[subject].min(),
                df[subject].max(),
                1,
                value=[df[subject].min(), df[subject].max()],
                marks={str(i): str(i) for i in df[subject]},
                id='subject-slider'
            ),
    else:
        return None


@app.callback(
    Output('year-century-dropdown-container', 'children'),
    Input('year-century-subject-dropdown', 'value'),
    Input('year-century-slider', 'value'),
    Input('year-slider', 'value'),
    Input('year-century-dropdown', 'value'),
    Input('year-hover', 'value')
)
def update_year_century_output(selected_subject, selected_century, selected_year, selected_dropdown, selected_hover):
    return dcc.Graph(figure=figures.create_year_cent_figure(selected_subject, selected_century, selected_year,
                                                            selected_dropdown, selected_hover), id='year-century-graph')


# century-graph
@app.callback(
    Output('century-dropdown-container', 'children'),
    Input('year-century-subject-dropdown', 'value'),
    Input('year-century-slider', 'value'),
)
def update_century_output(selected_subject, selected_century):
    return dcc.Graph(figure=figures.create_cent_figure(selected_subject, selected_century), id='century-graph')


@app.callback(
    Output('timeline-table-container', 'children'),
    Input('year-century-subject-dropdown', 'value'),
)
def update_timeline_table(selected_subject):
    df, subject, name = figures.get_variables(selected_subject)
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        page_action='none',
        fixed_rows={'headers': True},
        style_table={'overflowY': 'auto'},
        style_header={'backgroundColor': 'white', 'color': 'black'},
        style_data={'backgroundColor': 'lightblue', 'color': 'white'},
        id='timeline-table'
    )


@app.callback(
    Output('timeline-information', 'children'),
    Input('year-century-graph', 'hoverData'),
    #Input('year-century-subject-dropdown', 'value'),
    #Input('year-century-slider', 'value'),
    #Input('year-slider', 'value'),
    #Input('year-century-dropdown', 'value'),
    #Input('year-hover', 'value'),
)
def update_timeline_information(year_graph):#(year_graph, selected_subject, selected_century, selected_year, selected_dropdown, selected_hover):
    """html.Table(
        html.Tr(
            html.Td('Subject'),
            html.Td(selected_subject),
        )
    )"""
    return 0

"""
@app.callback(
    Output('hover-data', 'children'),
    Input('year-century-graph', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)
@app.callback(
    Output('click-data', 'children'),
    Input('year-century-graph', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)

@app.callback(
    Output('selected-data', 'children'),
    Input('year-century-graph', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)

@app.callback(
    Output('relayout-data', 'children'),
    Input('year-century-graph', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)
"""

# subject-graph
@app.callback(
    Output('subject-dropdown-container', 'children'),
    Input('subject-dropdown', 'value')
)
def update_subject_output(selected_subject):
    return dcc.Graph(figure=figures.create_subject_info_graph(selected_subject), id='subject-graph')

"""
@app.callback(
    Output(),
    Input(),
)
def
"""
if __name__ == '__main__':
    app.run_server(debug=True)