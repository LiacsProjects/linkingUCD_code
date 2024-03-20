#
# Imports
#
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import configparser
import os

#
# Imports
#
import dash
from dash import dcc, html, Input, Output, State, callback, ctx, dash_table, ALL
import dash_bootstrap_components as dbc

from Plugins.globals import data, SUBJECT_AREA_COLUMN_NAME, THESIS_COLUMN_NAME
from Plugins.helpers import select_range, select_non_range

from Plugins.Pages.Individual import individualgraphs
from Plugins.Pages.Geographic import geographygraphs

#
# Configure dash page
#
dash.register_page(
    __name__,
    title="Individual Professors",
    description="Visuals for aggregated individual data about professors",
    path="/pages/individual",
    order=3
)

#
# Layout
#
layout = html.Div(
    id='p_individual',
    className='container',
    children=[
        html.Div(id='p_Professor_header', className='page_header', children=[
            html.H1('Professors')
        ]),
        html.Div(id='p_i_inputs_left', className='middle_small_container ', children=[
            html.H3('Search settings:', className='inline'),

            html.Br(),
            html.P('Search for a name:', className='inline'),
            dcc.Input(
                id='p-search-name',
                type='text',
                placeholder='Search name',
                style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
                className='inline',
            ),
            dcc.RadioItems(
                inline=True,
                options=['Contains', 'Equals'],
                value='Contains',
                id='p-search-option',
                className='inline'
            ),
            html.Br(),
            html.P('Select appointment year range:', className='inline'),
            html.Br(),
            dcc.Input(
                id='appointment-min-input', className='inline',
                type='number',
                min=data.all_dates_df['year'].min(),
                max=data.all_dates_df['year'].max() - 1,
                value=data.all_dates_df['year'].min(),
                style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
            ),
            dcc.Input(
                id='appointment-max-input', className='inline',
                type='number',
                min=data.all_dates_df['year'].min() + 1,
                max=data.all_dates_df['year'].max(),
                value=data.all_dates_df['year'].max(),
                style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
            ),
            html.Br(),
            html.P('Select birthyear range:', className='inline'),
            html.Br(),
            dcc.Input(
                id='p-birthyear-min-input', className='inline',
                type='number',
                min=data.birth_df['year'].min(),
                max=data.birth_df['year'].max() - 1,
                value=data.birth_df['year'].min(),
                style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
            ),
            dcc.Input(
                id='p-birthyear-max-input', className='inline',
                type='number',
                min=data.all_dates_df['year'].min() + 1,
                max=data.all_dates_df['year'].max(),
                value=data.all_dates_df['year'].max(),
                style={'background-color': 'rgba(223,223,218,0.7)', 'color': 'black', 'margin': '1%'},
            ),
            html.Br(),
            html.P('Include people with missing date values? ', className='inline'),
            dcc.RadioItems(
                inline=True,
                options=['Yes', 'No'],
                value='Yes',
                id='p-include-missing-dates',
                className='inline',
            ),
            html.Br(),
            html.Br(),
            html.Button(
                'START SEARCH',
                id='p-search-individual',
                className='inline',
                style={'font-weight': 'bold', 'margin-left': '20%', 'height': '75px', 'width': '200px'},
            ),
        ]),
        html.Div(id='p_i_inputs_right', className='middle_small_container ', children=[
            html.Table([
                html.Tr([
                    html.Td(html.P('Select Gender:', className='inline'), ),
                    html.Td(dcc.Dropdown(individualgraphs.get_unique_values('Gender'), placeholder='Choose a gender',
                                         clearable=False, multi=True, id='p-individual-gender-dropdown',
                                         className='dropdown', style={"width": "400px"}), ),
                ]),
                html.Tr([
                    html.Td(html.P('Select birth place:', className='inline'), ),
                    html.Td(dcc.Dropdown(individualgraphs.get_unique_values('Birth place'),
                                         placeholder='Choose a birth place', clearable=False, multi=True,
                                         id='p-individual-birthplace-dropdown', className='dropdown',
                                         style={"width": "400px"}), ),
                ]),
                html.Tr([
                    html.Td(html.P('Select birth country:', className='inline'), ),
                    html.Td(dcc.Dropdown(individualgraphs.get_unique_values('Birth country'),
                                         placeholder='Choose a birth country', clearable=False, multi=True,
                                         id='p-individual-birthcountry-dropdown', className='dropdown',
                                         style={"width": "400px"}), ),
                ]),
                html.Tr([
                    html.Td(html.P('Select death place:', className='inline'), ),
                    html.Td(
                        dcc.Dropdown(individualgraphs.get_unique_values('Death place'), placeholder='Choose a death place',
                                     clearable=False, multi=True, id='p-individual-deathplace-dropdown',
                                     className='dropdown', style={"width": "400px"}), ),
                ]),
                html.Tr([
                    html.Td(html.P('Select death country:', className='inline'), ),
                    html.Td(dcc.Dropdown(individualgraphs.get_unique_values('Death country'),
                                         placeholder='Choose a death country', clearable=False, multi=True,
                                         id='p-individual-deathcountry-dropdown', className='dropdown',
                                         style={"width": "400px"}), ),
                ]),
                html.Tr([
                    html.Td(html.P('Select promotion:', className='inline'), ),
                    html.Td(dcc.Dropdown(individualgraphs.get_unique_values('Promotion'),
                                         placeholder='Choose a promotion', clearable=False, multi=True,
                                         id='p-individual-promotion-dropdown', className='dropdown',
                                         style={"width": "400px"}), ),
                ]),
                html.Tr([
                    html.Td(html.P('Select promotion place:', className='inline'), ),
                    html.Td(dcc.Dropdown(individualgraphs.get_unique_values('Promotion place'),
                                         placeholder='Choose a promotion place', clearable=False, multi=True,
                                         id='p-individual-promotionplace-dropdown', className='dropdown',
                                         style={"width": "400px"}), ),
                ]),
                html.Tr([
                    html.Td(html.P('Select thesis:', className='inline'), ),
                    html.Td(dcc.Dropdown(individualgraphs.get_unique_values('Thesis'), placeholder='Choose a thesis',
                                         clearable=False, multi=True, optionHeight=120, id='p-individual-thesis-dropdown',
                                         className='dropdown', style={"width": "400px"}), ),
                ]),
                html.Tr([
                    html.Td(html.P('Select job:', className='inline'), ),
                    html.Td(dcc.Dropdown(individualgraphs.get_unique_values('Job'), placeholder='Choose a job',
                                         clearable=False, multi=True, id='p-individual-job-dropdown', className='dropdown',
                                         style={"width": "400px"}), ),
                ]),
                html.Tr([
                    html.Td(html.P('Select subject area:', className='inline'), ),
                    html.Td(dcc.Dropdown(individualgraphs.get_unique_values('Subject area'),
                                         placeholder='Choose a subject area', clearable=False, multi=True, optionHeight=50,
                                         id='p-individual-subjectarea-dropdown', className='dropdown',
                                         style={"width": "400px"}), ),
                ]),
                html.Tr([
                    html.Td(html.P('Select faculty:', className='inline'), ),
                    html.Td(dcc.Dropdown(individualgraphs.get_unique_values('Faculty'), placeholder='Choose a faculty',
                                         clearable=False, multi=True, id='p-individual-faculty-dropdown',
                                         className='dropdown', style={"width": "400px"}), ),
                ]),
            ]),
        ]),
        html.Div(id='p-individual-information', className='middle_container', children=[
            html.A(id='p-search-results'),
            html.H3(id='p-individual-search-results-header', ),
            html.Div(id='p-individual-search-results', children=[
                html.Div(id='p-individual-search-results-number', className='inline', style={"font-weight": "bold"}),
                html.Div(id='p-individual-search-text', className='inline', style={'margin-left': '8px'})
            ]),
            html.Div(id='p-individual-table-container'),
            html.Div(id='p-individual-detailed-information', children=[
                html.Div(id='p-chosen-individual-information', children=[]),
                html.Div(id='p-chosen-individual-information-output'),
            ]),
            html.Div(id='p-individual-output'),
        ]),
    ]),

#
# Individual information callbacks
#
@callback(
    Output('p-individual-search-results-header', 'children'),
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
    prevent_initial_call=False,
)
def update_professor_table(search_button, selected_name, search_option, min_enrol, max_enrol, min_birth, max_birth,
                           include_missing, selected_gender, selected_birthplace, selected_birthcountry,
                           selected_deathplace, selected_deathcountry, selected_promotion, selected_promotionplace,
                           selected_thesis, selected_job, selected_subjectarea, selected_faculty):

    df = data.individual_profs_df[['First name', 'Last name', 'Gender', 'Appointment date', 'Appointment year',
                                   'Birth date', 'Birth year', 'Birth place', 'Birth country', 'Death date',
                                   'Death year', 'Death place', 'Death country', 'Promotion', 'Promotion place',
                                   'Promotion date', 'Promotion year', 'Thesis', 'Job', 'Subject area', 'Faculty',
                                   'Rating']]
    search_results_number = 0
    if ctx.triggered_id == 'p-search-individual':
        filtered_df = df.copy()  # deep=False?
        if selected_name is not None and selected_name != '':
            words = selected_name.split(' ')
            temp_total_df = pd.DataFrame()
            for word in words:
                # TODO: sort on relevance
                if search_option == 'Contains':
                    contains_df = df.loc[df['First name'].str.contains(str(word), case=False)]
                    contains_df1 = df.loc[df['Last name'].str.contains(str(word), case=False)]
                    temp_total_df = pd.concat([contains_df, contains_df1], ignore_index=True)
                elif search_option == 'Equals':
                    equals_df = df.loc[df['First name'] == str(word)]
                    equals_df1 = df.loc[df['Last name'] == str(word)]
                    temp_total_df = pd.concat([equals_df, equals_df1], ignore_index=True)

            if len(temp_total_df) > 0:  # If there are hits found, copy to filtered_df
                filtered_df = temp_total_df.copy()
                # filtered_df = pd.merge(filtered_df, temp_total_df, how='inner')
            else:  # No results, filtered_df is empty df
                # filtered_df = pd.DataFrame()
                filtered_df = pd.DataFrame(
                    columns=['First name', 'Last name', 'Gender', 'Appointment date', 'Appointment year', 'Birth date',
                             'Birth year', 'Birth place', 'Birth country', 'Death date', 'Death year', 'Death place',
                             'Death country',
                             'Promotion', 'Promotion place', 'Promotion date', 'Promotion year', 'Thesis', 'Job',
                             'Subject area', 'Faculty', 'Rating'])

        if min_enrol is not None and max_enrol is not None:
            filtered_df = select_range(filtered_df, min_enrol, max_enrol, 'Appointment year', include_missing)

        if min_birth is not None and max_enrol is not None:
            filtered_df = select_range(filtered_df, min_birth, max_birth, 'Birth year', include_missing)

        # selected_non_ranges = [selected_gender, selected_birthplace, selected_birthcountry, selected_deathplace,
        # selected_deathcountry, selected_promotion,
        #               selected_promotionplace, selected_thesis, selected_job, selected_subjectarea, selected_faculty]

        # for selected_non_range in selected_non_ranges:
        #     if selected_non_ranges is not None and select_non_range !=[]:
        #         filtered_df = select_non_range(filtered_df, selected_gender, ?)

        if selected_gender is not None and selected_gender != []:
            filtered_df = select_non_range(filtered_df, selected_gender, 'Gender')

        if selected_birthplace is not None and selected_birthplace != []:
            filtered_df = select_non_range(filtered_df, selected_birthplace, 'Birth place')

        if selected_birthcountry is not None and selected_birthcountry != []:
            filtered_df = select_non_range(filtered_df, selected_birthcountry, 'Birth country')

        if selected_deathplace is not None and selected_deathplace != []:
            filtered_df = select_non_range(filtered_df, selected_deathplace, 'Death place')

        if selected_deathcountry is not None and selected_deathcountry != []:
            filtered_df = select_non_range(filtered_df, selected_deathcountry, 'Death country')

        if selected_promotion is not None and selected_promotion != []:
            filtered_df = select_non_range(filtered_df, selected_promotion, 'Promotion')

        if selected_promotionplace is not None and selected_promotionplace != []:
            filtered_df = select_non_range(filtered_df, selected_promotionplace, 'Promotion place')

        if selected_thesis is not None and selected_thesis != []:
            filtered_df = select_non_range(filtered_df, selected_thesis, 'Thesis')

        if selected_job is not None and selected_job != []:
            filtered_df = select_non_range(filtered_df, selected_job, 'Job')

        if selected_subjectarea is not None and selected_subjectarea != []:
            filtered_df = select_non_range(filtered_df, selected_subjectarea, 'Subject area')

        if selected_faculty is not None and selected_faculty != []:
            filtered_df = select_non_range(filtered_df, selected_faculty, 'Faculty')

        search_results_header = "Professor search data:"
        search_results_number = len(filtered_df)
        if search_results_number == 1:
            text = "professor was found"
        else:
            text = "professors were found"
        text = text + " (make selection for individual information placed under the search table)"
        return search_results_header, search_results_number, text, dash_table.DataTable(
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

            css=[{
                'selector': '.dash-table-tooltip',
                'rule': 'background-color: #001158; font-family: monospace; color: white'
            }],
            tooltip_header={i: i for i in filtered_df.columns},
            tooltip_data=[{
                THESIS_COLUMN_NAME: {'value': str(row[THESIS_COLUMN_NAME]), 'type': 'markdown'},
                SUBJECT_AREA_COLUMN_NAME: {'value': str(row[SUBJECT_AREA_COLUMN_NAME]), 'type': 'markdown'},
            } for row in filtered_df.to_dict('records')
            ],
            tooltip_duration=None,
            tooltip_delay=0,

            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'line-height': '15px'
            },
            style_header={'backgroundColor': '#001158', 'color': 'white', 'fontWeight': 'bold'},
            style_data={
                # 'whiteSpace': 'normal',
                'backgroundColor': 'white',
                'color': 'black',
            },
            style_cell_conditional=[
                {'if': {'column_id': THESIS_COLUMN_NAME},
                 'maxWidth': '240px', 'textOverflow': 'ellipsis', 'overflow': 'hidden', },
                {'if': {'column_id': SUBJECT_AREA_COLUMN_NAME},
                 'maxWidth': '180px', 'textOverflow': 'ellipsis', 'overflow': 'hidden', },
            ],

            # virtualization=True,
            #            export_format='xlsx',
            #            export_headers='display',
            merge_duplicate_headers=True,
            id='p-individual-table'
        )
    else:
        return None, None, None, None

#
# Chosen person information
#
@callback(
    Output('p-chosen-individual-information', 'children'),
    #Input('p-individual-table', "derived_virtual_data"),
    #Input('p-individual-table', "derived_virtual_selected_rows"),
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

    # None type causes error, return "children" instead
    if selected_rows is None:
        return children
    for number in selected_rows:
        if number not in in_list:
            person = persons.iloc[number].to_frame().T
            figure = geographygraphs.create_map(person['Birth place'][number], person['Birth country'][number],
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
                                      # html.A('Go to globe', href='/assets/mapboxLeiden.html', target='_blank',
                                      # rel='noreferrer noopener'),
                                      # TODO: Implement family tree, not yet chosen which
                                      #  tree fits best: choices: 1. fisher_crawford (r implementation) 2. graphviz
                                      #  3. igraph
                                      dcc.Graph(figure=figure, id='p-life-map')
                                  ])
            children.append(new_person)
    return children

#
# Appointment input sync
#
@callback(
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

#
# Birthyear input sync
#
@callback(
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
