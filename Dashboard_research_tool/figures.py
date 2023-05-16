# Creating dataframe
from dash import dcc, html, dash_table
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from Adapters import database


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


def create_pivot_table(values, columns, index, aggfunc, graph_type):
    aggfunc = aggfunc[0].lower()

    if not values:
        values = []
    if not columns:
        columns = []
    if not index:
        index = []

    conn = database.Connection()
    df, pivot_table = conn.QueryBuilderPivotTable(index, values, columns, aggfunc)
    # print(df, pivot_table)
    # print(pd.pivot_table(df, values, index, columns, aggfunc))
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
    # print(type(dash_pivot_table))

    # dash_pivot_table = dash_table.DataTable(
    #         id='datatable-interactivity',
    #         columns=[
    #             {"name": i, "id": i, "deletable": True, "selectable": True} for i in pivot_table.columns
    #         ],
    #         data=pivot_table.reset_index().to_dict('records'),
    #         editable=True,
    #         filter_action="native",
    #         sort_action="native",
    #         sort_mode="multi",
    #         column_selectable="single",
    #         row_selectable="multi",
    #         row_deletable=True,
    #         selected_columns=[],
    #         selected_rows=[],
    #         page_action="native",
    #         page_current=0,
    #         page_size=10,
    #     )
    print(charts[0])
    print(dash_pivot_table)
    return dash_pivot_table, charts
