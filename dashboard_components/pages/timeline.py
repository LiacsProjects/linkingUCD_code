# import modules
from dash import Dash, dcc, html, Input, Output, ctx, dash_table, State, ALL, callback
import dash
from dashboard_components.pages import professorvisuals
from dashboard_components import data
from dashboard_components.figures_components import professorfigures  # , studentfigures, rectorfigures, introfigures

# from pages import professorvisuals, rectorvisuals, studentvisuals

# Parameters and constants
YEAR_STEP = 5
MARK_SPACING = 10

dash.register_page(__name__, path='/timeline')

# ******************************************************************************************  START
layout = professorvisuals.timeline


# Year slider
@callback(
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
    min_year = current_century['year'].min()
    max_year = current_century['year'].max()
    value = [current_century['year'].min(), current_century['year'].max()]
    marks: dict = {str(year): str(year) for year in
                   range(min_year, max_year, int((max_year - min_year) / MARK_SPACING))}
    return min_year, max_year, value, marks


# year-century graph
@callback(
    Output('p-year-century-graph', 'figure'),
    Input('p-year-century-subject-dropdown', 'value'),
    Input('p-year-century-slider', 'value'),
    Input('p-year-slider', 'value'),
    Input('p-year-century-dropdown', 'value'),
    running=[
        (Output('p-year-century-subject-dropdown', 'disabled'), True, False),
    ],
)
def update_year_century_output(selected_subject, selected_century, selected_year, selected_dropdown):
    figure = professorfigures.create_year_cent_figure(
        selected_subject,
        selected_century,
        selected_year,
        selected_dropdown)
    return figure


# century-graph
@callback(
    Output('p-century-graph', 'figure'),
    Input('p-year-century-subject-dropdown', 'value'),
    Input('p-year-century-slider', 'value'),
)
def update_century_output(selected_subject, selected_century):
    figure = professorfigures.create_cent_figure(selected_subject, selected_century)
    return figure


# Timeline information
@callback(
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
        if not 'customdata' in figure['data'][0].keys():
            return
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
                html.Td('Year with highest value'),
                html.Td(df.loc[df['count'] == df['count'].max(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Least appointments'),
                html.Td(df['count'].min()),
            ]),
            html.Tr(children=[
                html.Td('Year with lowest value'),
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
                html.Td('Year with highest value'),
                html.Td(df.loc[df['count'] == df['count'].max(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Least appointments'),
                html.Td(df['count'].min()),
            ]),
            html.Tr(children=[
                html.Td('Year with lowest value'),
                html.Td(df.loc[df['count'].min(), 'year']),
            ]),
            html.Tr(children=[
                html.Td('Average appointments'),
                html.Td(round(df['count'].mean(), 0)),
            ]),
        ]),
