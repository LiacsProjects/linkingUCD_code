# Creating dataframe
from dash import dcc, html, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
from Adapters import database
import dash_bootstrap_components as dbc
import math
import networkx as nx
from fuzzywuzzy import fuzz, process
import numpy as np

path = "D:/documents/uni/thesis/code_for_github/linkingUCD_code_latest/Dashboard_research_tool/pages/"
rl_df = pd.read_csv(
    path + 'genealogical_visualisation/RL Gelinkte Personen.csv',
    sep=';')
relations_df = pd.read_csv(
    path + 'genealogical_visualisation/relations_all.csv')
all_names = rl_df['name'].unique()
cities_coords = pd.read_excel(
    path + "geographic_visualisation/cities_coordinates.xlsx")
iso_alpha_df = pd.read_csv(
    path + "geographic_visualisation/iso_alpha.csv"
)


def find_closest_string_match(input_string, string_list):
    closest_match = process.extractOne(input_string, string_list)
    return closest_match[0]


def convert_html_to_dash(html_code):
    """Convert standard html to Dash components"""
    from xml.etree import ElementTree
    import dash_html_components as html

    def parse_css(css):
        """Convert a style in ccs format to dictionary accepted by Dash"""
        return {k: v for style in css.strip(";").split(";") for k, v in [style.split(":")]}

    def _convert(elem):
        comp = getattr(html, elem.tag.capitalize())
        children = [_convert(child) for child in elem]
        if not children:
            children = elem.text
        attribs = elem.attrib.copy()
        if "class" in attribs:
            attribs["className"] = attribs.pop("class")
        attribs = {k: (parse_css(v) if k == "style" else v) for k, v in attribs.items()}

        return comp(children=children, **attribs)

    et = ElementTree.fromstring(html_code)

    return _convert(et)


def create_pivot_table(values, columns, index, aggfunc, graph_type, filter_inputs, filter_labels, filter_exclude):
    # return errors
    if not aggfunc:
        return "Aggregate Function can not be empty.", None
    if not graph_type:
        return "Chart Type can not be empty.", None
    aggfunc = aggfunc[0].lower()

    filters = zip(filter_labels, filter_inputs)

    if not columns and not index:
        return "At least one 'Columns' or 'Index' is required.", None

    if not values:
        return "'Values' can not be empty.", None
    if not columns:
        columns = []
    if not index:
        index = []
    attributes = index + columns + values

    # make database connection
    conn = database.Connection()

    df, pivot_table = conn.QueryBuilderPivotTable(index, values, columns, aggfunc)

    for attribute in attributes:
        if 'Date' in attribute:
            df = df.dropna()
            df[attribute] = df[attribute].str[:4]
            df[attribute] = df[attribute].astype('int')
        if 'Type' in attribute:
            type_of = attribute[6:].lower()
            type_faculty_df = conn.select(f'type_of_{type_of}', '*', '')
            for type_value in df[attribute].unique():
                try:
                    df[attribute] = df[attribute].replace(type_value, type_faculty_df.loc[type_value][0])
                except KeyError:
                    continue

    # apply filters
    counter = 0
    for filter_tuple in filters:
        if filter_tuple[1] and filter_tuple[0] != 'Minimum threshold' and filter_tuple[0] != 'Maximum threshold':
            filter_exclude_bool = filter_exclude[counter]
            if not filter_exclude_bool:
                filter_inputs = filter_tuple[1].split(';')
                df = df[df[filter_tuple[0]].isin(filter_inputs)]
            else:
                filter_inputs = filter_tuple[1].split(';')
                df = df[~df[filter_tuple[0]].isin(filter_inputs)]
        if filter_tuple[0] == 'Minimum threshold':
            if filter_tuple[1]:
                minimum_threshold = int(filter_tuple[1])
            else:
                minimum_threshold = None
        elif filter_tuple[0] == 'Maximum threshold':
            if filter_tuple[1]:
                maximum_threshold = int(filter_tuple[1])
            else:
                maximum_threshold = None

        counter += 1

    if df.empty:
        return "Empty Data Selection", None
    pivot_table = pd.pivot_table(df, index=index, columns=columns, values=values, aggfunc=aggfunc)

    if minimum_threshold:
        pivot_table_row_sum = pivot_table.sum(axis=1)
        pivot_table = pivot_table.loc[list(pivot_table_row_sum[pivot_table_row_sum > minimum_threshold].index)]
    if maximum_threshold:
        pivot_table_row_sum = pivot_table.sum(axis=1)
        pivot_table = pivot_table.loc[list(pivot_table_row_sum[pivot_table_row_sum < maximum_threshold].index)]

    del conn

    # make html table
    pivot_table_html = pivot_table.to_html()
    pivot_table_html = pivot_table_html.replace("colspan", "colSpan")
    pivot_table_html = pivot_table_html.replace('halign="left"', '')
    pivot_table_html = pivot_table_html.replace('border="1"', '')
    pivot_table_html = pivot_table_html.replace('valign="top"', '')
    pivot_table_html = pivot_table_html.replace('rowspan', 'rowSpan')
    pivot_table_html = pivot_table_html.replace('NaN', '')

    pd.options.plotting.backend = "plotly"
    dash_pivot_table = convert_html_to_dash(pivot_table_html)

    charts = []

    try:
        # for every value create a new chart
        for value in values:

            # columns > 0 and index = 0
            if columns and not index:
                # columns = 2 and index = 0
                if len(columns) > 1:

                    column = columns[0]
                    column_values = df[column].unique()
                    column_values = [x for x in column_values if str(x) != 'nan']
                    pivot_chart = make_subplots()
                    for column_value in column_values:
                        try:
                            for column in pivot_table[column_value].columns:
                                if graph_type == 'bar':
                                    subplot = go.Bar(x=[pivot_table[column_value].index[0]],
                                                     y=pivot_table[column_value][column].to_list(),
                                                     hovertext=column_value + ' - ' + column,
                                                     name=column_value + ' - ' + column)
                                elif graph_type == 'line':
                                    subplot = go.Line(x=[pivot_table[column_value].index[0]],
                                                      y=pivot_table[column_value][column].to_list(),
                                                      hovertext=column_value + ' - ' + column,
                                                      name=column_value + ' - ' + column)
                                elif graph_type == 'barh':
                                    subplot = go.Bar(x=[pivot_table[column_value].index[0]],
                                                     y=pivot_table[column_value][column].to_list(),
                                                     hovertext=column_value + ' - ' + column,
                                                     name=column_value + ' - ' + column)
                                elif graph_type == 'hist':
                                    subplot = go.Histogram(x=[pivot_table[column_value].index[0]],
                                                           y=pivot_table[column_value][column].to_list(),
                                                           hovertext=column_value + ' - ' + column,
                                                           name=column_value + ' - ' + column)
                                elif graph_type == 'box':
                                    subplot = go.Box(x=[pivot_table[column_value].index[0]],
                                                     y=pivot_table[column_value][column].to_list(),
                                                     hovertext=column_value + ' - ' + column,
                                                     name=column_value + ' - ' + column)
                                elif graph_type == 'area':
                                    subplot = go.Bar(x=[pivot_table[column_value].index[0]],
                                                     y=pivot_table[column_value][column].to_list(),
                                                     hovertext=column_value + ' - ' + column,
                                                     name=column_value + ' - ' + column)
                                elif graph_type == 'scatter':
                                    subplot = go.Scatter(x=[pivot_table[column_value].index[0]],
                                                         y=pivot_table[column_value][column].to_list(),
                                                         hovertext=column_value + ' - ' + column,
                                                         name=column_value + ' - ' + column, mode='markers')
                                pivot_chart.add_trace(subplot)
                        except KeyError as e:
                            print(e)
                        pivot_chart.update_layout(barmode='stack')

                # columns = 1 and index = 0
                elif len(columns) == 1:
                    pivot_chart = pivot_table.plot(kind=graph_type)

            # columns = 0 and index > 0
            elif not columns and index:
                # columns = 0 and index = 2
                if len(index) > 1 and len(columns) == 0:
                    pivot_chart = make_subplots()
                    x_list = [str(i) for i in pivot_table[value].index.tolist()]
                    pivot_chart.add_trace(go.Bar(x=x_list, y=pivot_table[value].values))

                # columns = 0 and index = 1
                elif len(index) == 1:
                    pivot_chart = pivot_table[value].plot(kind=graph_type)

            # columns = 1 and index = 1
            elif len(index) == 1 and len(columns) == 1:
                pivot_chart = pivot_table[value].plot(kind=graph_type)

            # columns = 2 and index = 1
            elif len(index) == 1 and len(columns) > 1:
                column = columns[0]
                column_values = df[column].unique()
                column_values = [x for x in column_values if str(x) != 'nan']
                pivot_chart = make_subplots()
                for column_value in column_values:
                    try:
                        for column in pivot_table[value][column_value].columns:
                            if graph_type == 'bar':
                                subplot = go.Bar(x=pivot_table[value][column_value].index,
                                                 y=pivot_table[value][column_value][column].to_list(),
                                                 hovertext=column_value + ' - ' + column,
                                                 name=column_value + ' - ' + column)

                            elif graph_type == 'line':
                                subplot = go.Line(x=pivot_table[value][column_value].index,
                                                  y=pivot_table[value][column_value][column].to_list(),
                                                  hovertext=column_value + ' - ' + column,
                                                  name=column_value + ' - ' + column)
                            elif graph_type == 'barh':
                                subplot = go.Bar(x=pivot_table[value][column_value].index,
                                                 y=pivot_table[value][column_value][column].to_list(),
                                                 hovertext=column_value + ' - ' + column,
                                                 name=column_value + ' - ' + column)
                            elif graph_type == 'hist':
                                subplot = go.Histogram(x=pivot_table[value][column_value].index,
                                                       y=pivot_table[value][column_value][column].to_list(),
                                                       hovertext=column_value + ' - ' + column,
                                                       name=column_value + ' - ' + column)
                            elif graph_type == 'box':
                                subplot = go.Box(x=pivot_table[value][column_value].index,
                                                 y=pivot_table[value][column_value][column].to_list(),
                                                 hovertext=column_value + ' - ' + column,
                                                 name=column_value + ' - ' + column)
                            elif graph_type == 'area':
                                subplot = go.Bar(x=pivot_table[value][column_value].index,
                                                 y=pivot_table[value][column_value][column].to_list(),
                                                 hovertext=column_value + ' - ' + column,
                                                 name=column_value + ' - ' + column)
                            elif graph_type == 'scatter':
                                subplot = go.Scatter(x=pivot_table[value][column_value].index,
                                                     y=pivot_table[value][column_value][column].to_list(),
                                                     hovertext=column_value + ' - ' + column,
                                                     name=column_value + ' - ' + column, mode='markers')
                            pivot_chart.add_trace(subplot)
                    except KeyError as e:
                        print(e)
                pivot_chart.update_layout(barmode='stack')

            # columns = 1 and index = 2
            elif len(index) > 1 and len(columns) == 1:
                column = columns[0]
                column_values = df[column].unique()
                column_values = [x for x in column_values if str(x) != 'nan']
                pivot_chart = make_subplots()
                for column in pivot_table[value].columns:
                    if graph_type == 'bar':
                        x_list = [str(i) for i in pivot_table[value].index.tolist()]
                        subplot = go.Bar(x=x_list, y=pivot_table[value][column].to_list(),
                                         hovertext=column, name=column)
                    elif graph_type == 'line':
                        x_list = [str(i) for i in pivot_table[value].index.tolist()]
                        subplot = go.Line(x=x_list, y=pivot_table[value][column].to_list(),
                                          hovertext=column, name=column)
                    elif graph_type == 'barh':
                        x_list = [str(i) for i in pivot_table[value].index.tolist()]
                        subplot = go.Line(x=x_list, y=pivot_table[value][column].to_list(),
                                          hovertext=column, name=column)
                    elif graph_type == 'hist':
                        x_list = [str(i) for i in pivot_table[value].index.tolist()]
                        subplot = go.Histogram(x=x_list, y=pivot_table[value][column].to_list(),
                                               hovertext=column, name=column)
                    elif graph_type == 'box':
                        x_list = [str(i) for i in pivot_table[value].index.tolist()]
                        subplot = go.Box(x=x_list, y=pivot_table[value][column].to_list(),
                                         hovertext=column, name=column)
                    elif graph_type == 'area':
                        x_list = [str(i) for i in pivot_table[value].index.tolist()]
                        subplot = go.Bar(x=x_list, y=pivot_table[value][column].to_list(),
                                         hovertext=column, name=column)
                    elif graph_type == 'scatter':
                        x_list = [str(i) for i in pivot_table[value].index.tolist()]
                        subplot = go.Scatter(x=x_list, y=pivot_table[value][column].to_list(),
                                             hovertext=column, name=column, mode='markers')

                    pivot_chart.add_trace(subplot)
                pivot_chart.update_layout(barmode='stack')

            # columns = 2 and index = 2
            elif len(index) > 1 and len(columns) > 1:
                column = columns[0]
                column_values = df[column].unique()
                column_values = [x for x in column_values if str(x) != 'nan']
                pivot_chart = make_subplots()
                for column_value in column_values:
                    try:
                        for column in pivot_table[value][column_value].columns:
                            if graph_type == 'bar':
                                x_list = [str(i) for i in pivot_table[value].index.tolist()]
                                subplot = go.Bar(x=x_list, y=pivot_table[value][column_value][column].to_list(),
                                                 hovertext=column_value + ' - ' + column,
                                                 name=column_value + ' - ' + column)

                            elif graph_type == 'line':
                                x_list = [str(i) for i in pivot_table[value].index.tolist()]
                                subplot = go.Line(x=x_list, y=pivot_table[value][column_value][column].to_list(),
                                                  hovertext=column_value + ' - ' + column,
                                                  name=column_value + ' - ' + column)
                            elif graph_type == 'barh':
                                x_list = [str(i) for i in pivot_table[value].index.tolist()]
                                subplot = go.Bar(x=x_list, y=pivot_table[value][column_value][column].to_list(),
                                                 hovertext=column_value + ' - ' + column,
                                                 name=column_value + ' - ' + column)
                            elif graph_type == 'hist':
                                x_list = [str(i) for i in pivot_table[value].index.tolist()]
                                subplot = go.Histogram(x=x_list, y=pivot_table[value][column_value][column].to_list(),
                                                       hovertext=column_value + ' - ' + column,
                                                       name=column_value + ' - ' + column)
                            elif graph_type == 'box':
                                x_list = [str(i) for i in pivot_table[value].index.tolist()]
                                subplot = go.Box(x=x_list, y=pivot_table[value][column_value][column].to_list(),
                                                 hovertext=column_value + ' - ' + column,
                                                 name=column_value + ' - ' + column)
                            elif graph_type == 'area':
                                x_list = [str(i) for i in pivot_table[value].index.tolist()]
                                subplot = go.Bar(x=x_list, y=pivot_table[value][column_value][column].to_list(),
                                                 hovertext=column_value + ' - ' + column,
                                                 name=column_value + ' - ' + column)
                            elif graph_type == 'scatter':
                                x_list = [str(i) for i in pivot_table[value].index.tolist()]
                                subplot = go.Scatter(x=x_list, y=pivot_table[value][column_value][column].to_list(),
                                                     hovertext=column_value + ' - ' + column,
                                                     name=column_value + ' - ' + column, mode='markers')
                            pivot_chart.add_trace(subplot)
                    except KeyError as e:
                        print(e)

                pivot_chart.update_layout(barmode='stack')

            pivot_chart.update_layout(width=1200, height=700, barmode='stack')
            dash_pivot_chart = dcc.Graph(figure=pivot_chart)
            charts.append(dash_pivot_chart)

    except TypeError as e:
        print(e)
        dash_pivot_chart = None

    return dash_pivot_table, charts


def create_city_map(data_selection, person_selection, year_selection, year_bool):
    # type of location 1 = geboorteplaats, 2 = sterfteplaats
    # type of person 1 = professor, 2 = student
    if data_selection == 'Birth City':
        type_of_location = 1
    elif data_selection == 'Death City':
        type_of_location = 2

    if person_selection == 'Professor':
        type_of_person = 1
    elif person_selection == 'Student':
        type_of_person = 2

    conn = database.Connection()
    df = conn.select('location', ['City', 'TypeOfPerson', 'locationStartDate'],
                     f"JOIN person ON person.personPersonID = location.locationPersonID WHERE TypeOfLocation = {type_of_location} AND person.TypeOfPerson = {type_of_person}")
    del conn

    if year_bool:
        df = df.dropna()
        df['locationStartDate'] = df['locationStartDate'].str[:4].astype(int)
        df = df[df['locationStartDate'] > year_selection[0]]
        df = df[df['locationStartDate'] < year_selection[1]]

    df_counted = df.index.value_counts()

    geo_df = pd.DataFrame()
    city_list = []
    city_count_list = []
    lon_list = []
    lat_list = []
    for city in df_counted.index:
        try:
            lat_list.append(cities_coords[cities_coords['City'] == city]['Latitudes'].to_list()[0])
            lon_list.append(cities_coords[cities_coords['City'] == city]['Longitudes'].to_list()[0])
            city_list.append(city)
            city_count_list.append(df_counted.loc[city])
        except IndexError:
            city_list.append(city)
            city_count_list.append(df_counted.loc[city])
            lat_list.append(None)
            lon_list.append(None)

    geo_df['City'] = city_list
    geo_df['Count'] = city_count_list
    geo_df['Longitude'] = lon_list
    geo_df['Latitude'] = lat_list

    fig = go.Figure()

    for row in geo_df.iterrows():
        fig.add_trace(go.Scattergeo(
            lon=[row[1]["Longitude"]],
            lat=[row[1]['Latitude']],
            text=str(row[1]['Count']),
            marker=dict(
                size=math.log(row[1]['Count'], 1.02) / 10,
                color='royalblue',
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area'
            ),
            name=row[1]['City']
        ))
    fig.update_layout(width=1200, height=700,
                      legend=dict(font=dict(size=10, color="black")))
    return fig


def create_country_map(data_selection, person_selection, year_selection, year_bool, scale_option):
    # type of location 1 = geboorteplaats, 2 = sterfteplaats
    # type of person 1 = professor, 2 = student
    if data_selection == 'Birth Country':
        type_of_location = 1
    elif data_selection == 'Death Country':
        type_of_location = 2

    if person_selection == 'Professor':
        type_of_person = 1
    elif person_selection == 'Student':
        type_of_person = 2

    conn = database.Connection()
    df = conn.select('location', ['Country', 'TypeOfPerson', 'locationStartDate'],
                     f"JOIN person ON person.personPersonID = location.locationPersonID WHERE TypeOfLocation = {type_of_location} AND person.TypeOfPerson = {type_of_person}")
    del conn

    if year_bool:
        df = df.dropna()
        df['locationStartDate'] = df['locationStartDate'].str[:4].astype(int)
        df = df[df['locationStartDate'] > year_selection[0]]
        df = df[df['locationStartDate'] < year_selection[1]]

    count_list = df.index.value_counts().to_list()
    log_count_list = []
    for count in count_list:
        log_count = math.log(count, 1.02)
        log_count_list.append(log_count)
    country_list = df.index.value_counts().index.to_list()

    # TODO iso alpha in de database ipv csv
    filtered_df = pd.DataFrame()
    filtered_df['country'] = country_list
    filtered_df['count'] = count_list
    filtered_df['log_count'] = log_count_list
    iso_alpha_list = []
    iso_alpha_df['country'] = iso_alpha_df['country'].str.lower()
    for country in country_list:
        try:
            iso_alpha = iso_alpha_df[iso_alpha_df['country'] == country.lower()]['iso_alpha'].to_list()[0]
            iso_alpha_list.append(iso_alpha)
        except IndexError:
            if "NL" in country:
                iso_alpha_list.append("NLD")
            iso_alpha_list.append(None)

    filtered_df['iso_alpha'] = iso_alpha_list
    print(filtered_df)

    fig = go.Figure()
    if scale_option == 'Log':
        fig.add_choropleth(locations=filtered_df['iso_alpha'],
                           z=filtered_df['log_count'],
                           text=filtered_df['country'],
                           colorscale='cividis',
                           autocolorscale=False,
                           reversescale=False)
    elif scale_option == 'Absolute':
        fig.add_choropleth(locations=filtered_df['iso_alpha'],
                           z=filtered_df['count'],
                           text=filtered_df['country'],
                           colorscale='cividis',
                           autocolorscale=False,
                           reversescale=False)

    fig.update_layout(height=700,
                      legend=dict(font=dict(size=10, color="black")))
    return fig


# relations van 1 individu vinden
def relations_to_person(unique_person_id):
    """
    Looks up one person in the rl_df, this person has many certificates to their name,
    these certificates are looked up in the relations_df, finding links between people
    the links are registered, and the id's (from the rl_df) are stored
    """

    person_data = rl_df[rl_df['unique_person_id'] == unique_person_id]
    names = list(person_data['name'].unique())

    relations = []
    relations_id = []
    counter = 0

    # edges is a list in this form [(unique_person_id_1, unique_person_id_2), relation_type, name_1, name_2, year]
    # the unique_person_id comes from the Rl Gelinkte Personen file
    edges = []

    for certificate in person_data['uuid']:
        # found an edge from the unique_person_id in this function to someone else
        if len(relations_df[relations_df['uuid_1'] == certificate]):
            # the relation in the relations_df
            relation = relations_df[relations_df['uuid_1'] == certificate]
            for single_relation in relation.iterrows():
                relations.append(single_relation[1])

                # the id from rl_df from the 'other' person in the relation
                uuid_2 = single_relation[1].loc['uuid_2']
                try:
                    unique_person_id_2 = int(rl_df[rl_df['uuid'] == uuid_2]['unique_person_id'])
                except TypeError:
                    unique_person_id_2 = None

                relations_id.append(unique_person_id_2)

                certificate_person_data = person_data[person_data['uuid'] == certificate]
                certificate_person_data_2 = rl_df[rl_df['unique_person_id'] == unique_person_id_2][
                    rl_df[rl_df['unique_person_id'] == unique_person_id_2]['uuid'] == uuid_2]

                edges.append([(unique_person_id, unique_person_id_2), single_relation[1]['relation_type'], (
                list(certificate_person_data['year']), list(certificate_person_data['name']),
                list(certificate_person_data_2['year']), list(certificate_person_data_2['name']))])

        # found an edge from someone else to the unique_person_id in this function
        if len(relations_df[relations_df['uuid_2'] == certificate]):
            # the relation in the relations_df
            relation = relations_df[relations_df['uuid_2'] == certificate]
            for single_relation in relation.iterrows():
                relations.append(single_relation[1])

                # the id from rl_df from the 'other' person in the relation
                uuid_2 = single_relation[1].loc['uuid_1']
                try:
                    unique_person_id_2 = int(rl_df[rl_df['uuid'] == uuid_2]['unique_person_id'])
                except TypeError:
                    unique_person_id_2 = None

                relations_id.append(unique_person_id_2)

                certificate_person_data = person_data[person_data['uuid'] == certificate]
                certificate_person_data_2 = rl_df[rl_df['unique_person_id'] == unique_person_id_2][
                    rl_df[rl_df['unique_person_id'] == unique_person_id_2]['uuid'] == uuid_2]

                edges.append([(unique_person_id_2, unique_person_id), single_relation[1]['relation_type'], (
                list(certificate_person_data_2['year']), list(certificate_person_data_2['name']),
                list(certificate_person_data['year']), list(certificate_person_data['name']))])
        counter += 1

    # edge[0][0] == child, edge[0][1] == parent
    return edges, relations_id


def find_edges(unique_person_id, depth, completed_ids):
    if unique_person_id not in completed_ids:
        edges, next_id_list = relations_to_person(unique_person_id)
        completed_ids.append(unique_person_id)
        depth -= 1
        if depth:
            for next_id in next_id_list:
                new_edges = find_edges(next_id, depth, completed_ids)
                if new_edges:
                    for new_edge in new_edges:
                        edges.append(new_edge)
        return edges


def create_network_fig(depth, start_person, layout, drawing_options):
    # return errors
    if not start_person:
        return "Start person can not be empty"
    if not depth:
        return "Depth can not be empty"
    if not layout:
        return "Layout can not be empty"

    try:
        start_person = int(start_person)
    except ValueError:
        start_person = find_closest_string_match(start_person, all_names)
        # TODO wat als er twee mensen met dezelfde naam zijn? ook heel langzaam
        start_person = list(rl_df[rl_df['name'] == start_person]['unique_person_id'].unique())[0]

    # find all edges
    edges_relations = find_edges(start_person, depth, [])

    processed_edges = []

    layer_dict = {}
    layer_dict.update({start_person: 0})

    # first create the graph with networkx and take note of which edges were added
    G = nx.Graph()
    for edge_relation in edges_relations:
        if edge_relation not in processed_edges and edge_relation[0][0] and edge_relation[0][1]:
            G.add_edge(*(edge_relation[0][0], edge_relation[0][1]))

            processed_edges.append(edge_relation)

    # update layer_dict which decides on which layer the nodes should be in the generational view
    for processed_edge in processed_edges:
        relation_type = processed_edge[1]
        relation_person_1 = processed_edge[0][0]
        relation_person_2 = processed_edge[0][1]

        if relation_person_1 in list(layer_dict.keys()):
            layer = layer_dict[relation_person_1]
            if relation_type == 'huwelijk' or relation_type == 'Overleden':
                layer_dict.update({relation_person_2: layer})
            elif relation_type == 'vader' or relation_type == 'moeder':
                layer_dict.update({relation_person_2: layer + 1})

        if relation_person_2 in list(layer_dict.keys()):
            layer = layer_dict[relation_person_2]
            if relation_type == 'huwelijk' or relation_type == 'Overleden':
                layer_dict.update({relation_person_1: layer})
            elif relation_type == 'vader' or relation_type == 'moeder':
                layer_dict.update({relation_person_1: layer - 1})

    for node_id in list(layer_dict.keys()):
        G.add_node(node_id, layer=layer_dict[node_id])

    # create node positions
    if layout == 'Generational view':
        pos = nx.multipartite_layout(G, subset_key='layer', align='horizontal')
    elif layout == 'Kamada-Kawai layout':
        pos = nx.kamada_kawai_layout(G)
    elif layout == 'Circular layout':
        pos = nx.circular_layout(G)
    elif layout == 'Spectral layout':
        pos = nx.spectral_layout(G)
    elif layout == 'Random layout':
        pos = nx.random_layout(G)

    mnode_x, mnode_y, mnode_txt = [], [], []

    edge_trace = []
    arrow_layouts = []

    edge_text_counter = 0

    # create the edges in the figure
    for edge in G.edges():
        relation_type = 'No relation type found'

        # additional information for every edge
        for processed_edge in processed_edges:
            if processed_edge[0] == edge or (processed_edge[0][1], processed_edge[0][0]) == edge:
                relation_type = str(processed_edge[1])
                relation_type_string = '<br>Relation type: ' + str(processed_edge[1])
                person_1_data = '<br>Person 1 ID: ' + str(processed_edge[0][0]) + '<br>Person 1 Name: ' + str(
                    processed_edge[2][1][0])
                person_2_data = '<br>Person 2 ID: ' + str(processed_edge[0][1]) + '<br>Person 2 Name: ' + str(
                    processed_edge[2][3][0])
                year = "Year: " + str(processed_edge[2][0])

                break

        edge_x = []
        edge_y = []

        if edge[0] == processed_edge[0][0]:
            x0, y0 = pos[edge[1]]
            x1, y1 = pos[edge[0]]
        else:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]

        arrow_x1 = (2 * x0 + 3.5 * x1) / 5.5
        arrow_y1 = (2 * y0 + 3.5 * y1) / 5.5

        if relation_type == "Overleden" and layout == "Generational view":
            y1 -= 0.02
        elif relation_type == "Overleden":
            y1 -= 0.05

        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

        if relation_type == 'huwelijk':
            mnode_x.extend([(x0 + x1) / 2])
            mnode_y.extend([(y0 + y1) / 2 + 0.01])
        elif relation_type == "vader" or relation_type == "moeder":
            mnode_x.extend([arrow_x1])
            mnode_y.extend([arrow_y1])
        else:
            mnode_x.extend([(x0 + x1) / 2])
            mnode_y.extend([(y0 + y1) / 2])

        if relation_type != "Overleden":
            mnode_txt.extend([year + person_1_data + person_2_data + relation_type_string])
        else:
            mnode_txt.extend([year + person_1_data + relation_type_string])

        edge_text_counter += 1

        if relation_type == 'vader' and 'vader' in drawing_options:
            edge_trace.append(go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=0.7, color='#6495ED'),
                hoverinfo='text',
                mode='lines',
            ))

            arrow_layouts.append(dict(
                x=arrow_x1,
                y=arrow_y1,
                xref='x',
                yref='y',
                text='',
                showarrow=True,
                axref='x', ayref='y',
                ax=x0,
                ay=y0,
                arrowhead=3,
                arrowsize=1.3,
                arrowwidth=2,
                arrowcolor='#6495ED'
            ))
        elif relation_type == "moeder" and 'moeder' in drawing_options:
            edge_trace.append(go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=0.7, color='#fc9df9'),
                hoverinfo='text',
                mode='lines',
            ))

            arrow_layouts.append(dict(
                x=arrow_x1,
                y=arrow_y1,
                xref='x',
                yref='y',
                text='',
                showarrow=True,
                axref='x', ayref='y',
                ax=x0,
                ay=y0,
                arrowhead=3,
                arrowsize=1.3,
                arrowwidth=2,
                arrowcolor='#fc9df9'
            ))
        elif relation_type == 'huwelijk' and 'huwelijk' in drawing_options:
            half_x = (x0 + x1) / 2
            half_y = (y0 + y1) / 2 + 0.01
            edge_x_1 = (x0, half_x)
            edge_y_1 = (y0, half_y)
            edge_x_2 = (half_x, x1)
            edge_y_2 = (half_y, y1)

            edge_trace.append(go.Scatter(
                x=edge_x_1, y=edge_y_1,
                line=dict(width=2, color='#daa520', shape='spline', smoothing=1.3),
                hoverinfo='text',
                mode='lines', ))
            edge_trace.append(go.Scatter(
                x=edge_x_2, y=edge_y_2,
                line=dict(width=2, color='#daa520', shape='spline', smoothing=1.3),
                hoverinfo='text',
                mode='lines', ))

        elif relation_type == 'Overleden' and 'Overleden' in drawing_options:
            edge_trace.append(go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=2, color='#000000'),
                hoverinfo='text',
                mode='lines', ))

    # text for hovering
    mnode_trace = go.Scatter(x=mnode_x, y=mnode_y, mode="markers", showlegend=False,
                             hovertext=mnode_txt, marker=go.Marker(opacity=0))

    # draw every node in the fig
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2),
    )

    # add node hover text
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        for processed_edge in processed_edges:
            if list(G.nodes())[node] == processed_edge[0][0]:
                node_name = processed_edge[2][1][0]
            elif list(G.nodes())[node] == processed_edge[0][1]:
                node_name = processed_edge[2][3][0]

        node_text.append(f'Person ID: {list(G.nodes())[node]}<br>Name: {node_name}<br>Number of connections: ' + str(
            len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    # create the figure
    fig = go.Figure(data=[node_trace],
                    layout=go.Layout(
                        hovermode='closest',
                        showlegend=False,
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        width=1200,
                        height=1000
                    ),
                    )
    for edge_trace_value in edge_trace:
        fig.add_trace(edge_trace_value)

    fig.add_trace(mnode_trace)

    for arrow_layout in arrow_layouts:
        fig.add_annotation(arrow_layout)

    return fig
