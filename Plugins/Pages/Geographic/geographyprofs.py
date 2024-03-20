#
# Imports
#
import dash
from dash import dcc, html, Input, Output, callback, ctx, dash_table
import dash_bootstrap_components as dbc

from Plugins.globals import data
from Plugins.globals import GRAPH_SUBJECT_DROPDOWN, DEFAULT_GRAPH_SUBJECT

#from Plugins.Data import exceldata as data
from Plugins.Pages.Geographic import geographygraphs

#
# Configure dash page
#
dash.register_page(
    __name__,
    title="Geography Professors",
    description="Visuals for aggregated geographical data about professors",
    path="/pages/geographic",
    order=4
)

#
# Global consts
#
GEOMAPS_OPTIONS = ['Heat map', 'Line map', 'MP Heat map', 'MP Scatter map', 'Animated map']

#
# Layout
#
layout = html.Div(
    id='g_geo',
    className='container',
    children=[
        html.Div(id='g_geo_header',
                 className='page_header',
                 children=[html.H1('Professors')]
                 ),

        html.Div(id='p-geo-map-container',
                 className='right_container',
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
                         clearable=False, id='p-geo-subject-dropdown',
                         className='dropdown'
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
                         style={'background-color': 'rgba(223,223,218,0.7)',
                                'color': 'black', 'margin': '1%'},
                     ),
                     html.P('Highest year', className='inline'),
                     dcc.Input(
                         id='p-geo-max-input', className='inline',
                         type='number',
                         min=data.all_dates_df['year'].min() + 1,
                         max=data.all_dates_df['year'].max(),
                         value=data.all_dates_df['year'].max(),
                         style={'background-color': 'rgba(223,223,218,0.7)',
                                'color': 'black', 'margin': '1%'},
                     ),
                 ]),

        html.Div(id='p-map-info',
                 className='left_container',
                 children=[
                    html.H3('Country information'),
                    html.Div(id='p-map-table-container'),
                 ]),
        ]),

#
# Geographical information callbacks
# Geo input sync
@callback(
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
@callback(
    Output('p-map-container', 'children'),
    Output('p-map-table-container', 'children'),
    Input('p-geo-min-input', 'value'),
    Input('p-geo-max-input', 'value'),
    Input('p-map-choice', 'value'),
)
def create_map(min_year, max_year, map_choice):
    if map_choice == 'Heat map':
        figure, geo_data = geographygraphs.create_country_map(min_year, max_year)
        geo_data = geo_data[['country', 'count']]
    elif map_choice == 'Line map':
        figure, geo_data = geographygraphs.create_country_line_map(min_year, max_year)
        geo_data = geo_data[['country', 'count']]
    elif map_choice == 'MP Heat map':
        figure, geo_data = geographygraphs.create_mapbox_heat_map(min_year, max_year)
        geo_data = geo_data[['country', 'count']]
    elif map_choice == 'MP Scatter map':
        figure, geo_data = geographygraphs.create_mapbox_scatter_map(min_year, max_year)
        geo_data = geo_data[['country', 'year', 'count']]
    elif map_choice == 'Animated map':
        figure, geo_data = geographygraphs.create_animated_country_map(min_year, max_year)
        geo_data = geo_data[['country', 'year', 'count']]
    else:
        figure, geo_data = geographygraphs.create_country_map(min_year, max_year)
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
