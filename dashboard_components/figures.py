# Creating dataframe
from dash import dcc, html, dash_table
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from Adapters import database
import dash_bootstrap_components as dbc
import math


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
                'C:/Users/boert/Documents/uni/thesis/code_for_github/linkingUCD_code/Dashboard/figures_components/cities_coordinates.xlsx',
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
    cities_coords = pd.read_excel("geographic_visualisation/cities_coordinates.xlsx")
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

#
# fig = create_map()
# fig.show()
