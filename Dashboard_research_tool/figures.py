# Creating dataframe
from dash import dcc, html, dash_table
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from Adapters import database
import dash_bootstrap_components as dbc
import math
import networkx as nx



rl_df = pd.read_csv(
    'H:/Documents/uni/thesis/code_for_github/linkingUCD_code/Dashboard_research_tool/pages/genealogical_visualisation/RL Gelinkte Personen.csv',
    sep=';')
relations_df = pd.read_csv(
    'H:/Documents/uni/thesis/code_for_github/linkingUCD_code/Dashboard_research_tool/pages/genealogical_visualisation/relations_all.csv')



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
    aggfunc = aggfunc[0].lower()

    filters = zip(filter_labels, filter_inputs)


    if not values:
        values = []
    if not columns:
        columns = []
    if not index:
        index = []

    conn = database.Connection()
    df, pivot_table = conn.QueryBuilderPivotTable(index, values, columns, aggfunc)
    print(df)
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

    pivot_table = pd.pivot_table(df, index=index, columns=columns, values=values, aggfunc=aggfunc)

    if minimum_threshold:
        pivot_table_row_sum = pivot_table.sum(axis=1)
        pivot_table = pivot_table.loc[list(pivot_table_row_sum[pivot_table_row_sum > minimum_threshold].index)]
    if maximum_threshold:
        pivot_table_row_sum = pivot_table.sum(axis=1)
        pivot_table = pivot_table.loc[list(pivot_table_row_sum[pivot_table_row_sum < maximum_threshold].index)]


    del conn

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

    # print(pivot_table)
    # print(pivot_table_html)

    try:
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
                                    # TODO barh
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
                                    # TODO area
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
                                # TODO barh
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
                                # TODO area
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
                        # TODO barh
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
                        # TODO area
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
                                # TODO barh
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
                                # TODO area
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
            # TODO customizable barmode
            # TODO geographic data visualisation
            # TODO filters
            # TODO database implementation
            # TODO make it so you cant select the same thing in index and column

            pivot_chart.update_layout(width=1200, height=700, barmode='stack')
            dash_pivot_chart = dcc.Graph(figure=pivot_chart)
            charts.append(dash_pivot_chart)

        if 'Birth place' in index and not columns:
            cities_coords_df = pd.read_excel(
                'C:/Users/boert/Documents/uni/thesis/code_for_github/linkingUCD_code/Dashboard/figures/cities_coordinates.xlsx',
                engine='openpyxl')

            counter = 0
            cities_list = []
            lons = []
            lats = []
            count = []

            for row_index in pivot_table[value].index:
                # print(row_index)
                # print(pivot_table[value].iloc[counter])
                cities_list.append(row_index)
                count.append(pivot_table[value].iloc[counter])
                lons.append(cities_coords_df[cities_coords_df['City'] == row_index]['Longitudes'].values[0])
                lats.append(cities_coords_df[cities_coords_df['City'] == row_index]['Latitudes'].values[0])
                counter += 1

            geo_df = pd.DataFrame()
            geo_df['City'] = cities_list
            geo_df['Count'] = count
            geo_df['Latitude'] = lats
            geo_df['Longitude'] = lons
            geo_fig = go.Figure(data=go.Scattergeo(
                lon=geo_df['Longitude'],
                lat=geo_df['Latitude'],
                text=geo_df['City'],
                marker=dict(
                    size=geo_df['Count'] * 2,
                    line_color='rgb(40,40,40)',
                    line_width=0.5,
                    sizemode='area',
                ),
            ))
            geo_fig.update_layout(width=1200, height=700)
            dash_geo_chart = dcc.Graph(figure=geo_fig)
            charts.append(dash_geo_chart)

    except TypeError as e:
        print(e)
        dash_pivot_chart = None

    # dash_pivot_table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, index=True)
    return dash_pivot_table, charts


def create_map():
    cities_coords = pd.read_excel("D:/documents/uni/thesis/code_for_github/linkingUCD_code/Dashboard_research_tool/pages/geographic_visualisation/cities_coordinates.xlsx")
    conn = database.Connection()
    df, pivot_table = conn.QueryBuilderPivotTable(['City'], ['TypeOfPerson'], [], 'count')
    counter = 0
    del conn

    filter = [1]
    if filter == [1]:
        scale = 10
    if filter == [1,2]:
        scale = 50
    if filter == [2]:
        scale = 30

    df = df[df['TypeOfPerson'].isin(filter)]
    pivot_table = pd.pivot_table(df, index=['City'], columns=[], values=['TypeOfPerson'], aggfunc='count')

    geo_df = pd.DataFrame()
    city_list = []
    city_count_list = []
    lon_list = []
    lat_list = []
    for city in pivot_table.index:
        try:
            lat_list.append(cities_coords[cities_coords['City'] == city]['Latitudes'].to_list()[0])
            lon_list.append(cities_coords[cities_coords['City'] == city]['Longitudes'].to_list()[0])
            city_list.append(city)
            city_count_list.append(pivot_table.loc[city]['TypeOfPerson'])
        except IndexError:
            city_list.append(city)
            city_count_list.append(pivot_table.loc[city]['TypeOfPerson'])
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
                size=math.log(row[1]['Count'], 1.02)/10,
                color='royalblue',
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area'
            ),
            name=row[1]['City']
        ))
    print('created fig')
    # return dcc.Graph(figure=fig)
    return fig


# fig = create_map()
# fig.show()

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
                    # print('typeerror', rl_df[rl_df['uuid'] == uuid_2]['unique_person_id'])
                    unique_person_id_2 = None

                relations_id.append(unique_person_id_2)

                # print(single_relation)
                # print(unique_person_id)
                # print(unique_person_id_2)
                # print(certificate)
                # print(uuid_2)

                certificate_person_data = person_data[person_data['uuid'] == certificate]
                certificate_person_data_2 = rl_df[rl_df['unique_person_id'] == unique_person_id_2][
                    rl_df[rl_df['unique_person_id'] == unique_person_id_2]['uuid'] == uuid_2]

                # print(type(certificate_person_data['year']))
                # print(certificate_person_data_2)

                edges.append([(unique_person_id, unique_person_id_2), single_relation[1]['relation_type'], (list(certificate_person_data['year']), list(certificate_person_data['name']), list(certificate_person_data_2['year']), list(certificate_person_data_2['name']))])
            # print('\n\n')

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
                    # print('typeerror', rl_df[rl_df['uuid'] == uuid_2]['unique_person_id'])
                    unique_person_id_2 = None

                relations_id.append(unique_person_id_2)

                # print(single_relation)
                # print(unique_person_id)
                # print(unique_person_id_2)
                # print(certificate)
                # print(uuid_2)

                certificate_person_data = person_data[person_data['uuid'] == certificate]
                certificate_person_data_2 = rl_df[rl_df['unique_person_id'] == unique_person_id_2][rl_df[rl_df['unique_person_id'] == unique_person_id_2]['uuid'] == uuid_2]

                # print(certificate_person_data)
                # print(certificate_person_data_2)

                edges.append([(unique_person_id_2, unique_person_id), single_relation[1]['relation_type'], (list(certificate_person_data_2['year']), list(certificate_person_data_2['name']), list(certificate_person_data['year']), list(certificate_person_data['name']))])
            # print('\n\n')
        counter += 1

    # edge[0][0] == child, edge[0][1] == parent
    return edges, relations_id


def find_edges(unique_person_id, depth, completed_ids):
    print(depth)
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


def create_network_fig(depth, start_person):
    relation_type_options = ['Overleden', 'huwelijk', 'vader', 'moeder']

    # find all edges
    edges_relations = find_edges(start_person, depth, [])

    processed_edges = []

    layer_dict = {}
    layer_dict.update({start_person: 0})
    # first create the graph with networkx
    G = nx.Graph()
    for edge_relation in edges_relations:

        if edge_relation not in processed_edges and edge_relation[0][0] and edge_relation[0][1]:
            G.add_edge(*(edge_relation[0][0], edge_relation[0][1]))

            processed_edges.append(edge_relation)

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

    print(layer_dict)

    for node_id in list(layer_dict.keys()):
        G.add_node(node_id, layer=layer_dict[node_id])



    # create positions
    # TODO based on user input
    print(G.nodes())

    pos = nx.multipartite_layout(G, subset_key='layer', align='horizontal')
    counter = 0
    for pos_value in pos:
        # print(pos[pos_value])
        # print(processed_edges[counter])
        # new_y_value = processed_edges[counter][2][0][0]-1800
        # pos[pos_value] = [pos[pos_value][0], new_y_value]

        counter += 1

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
                # print(processed_edge[0], edge, processed_edge[1])
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

        if relation_type == "Overleden":
            y1 -= 0.01

        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

        if relation_type == 'huwelijk':
            mnode_x.extend([(x0 + x1) / 2])
            mnode_y.extend([(y0 + y1) / 2 + 0.01])
        else:
            mnode_x.extend([arrow_x1])
            mnode_y.extend([arrow_y1])

        if relation_type != "Overleden":
            mnode_txt.extend([year + person_1_data + person_2_data + relation_type_string])
        else:
            mnode_txt.extend([year + person_1_data + relation_type_string])

        edge_text_counter += 1

        if relation_type == 'vader':
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
        elif relation_type == "moeder":
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
        elif relation_type == 'huwelijk':
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
                mode='lines',))
            edge_trace.append(go.Scatter(
                x=edge_x_2, y=edge_y_2,
                line=dict(width=2, color='#daa520', shape='spline', smoothing=1.3),
                hoverinfo='text',
                mode='lines',))

        elif relation_type == 'Overleden':
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

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        for processed_edge in processed_edges:
            if list(G.nodes())[node] == processed_edge[0][0]:
                node_name = processed_edge[2][1][0]
            elif list(G.nodes())[node] == processed_edge[0][1]:
                node_name = processed_edge[2][3][0]

        node_text.append(f'Person ID: {list(G.nodes())[node]}<br>Name: {node_name}<br>Number of connections: ' + str(len(adjacencies[1])))

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
