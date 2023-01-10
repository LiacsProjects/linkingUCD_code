# Project: Dashboard Leiden 1848 Ben van yperen
# Digital Humanities Special Topics
#
# *************************************************************** Initialisatie, libraries
# import Add_environment_variable
# import modules
import dash
import plotly.graph_objects as go
import plotly.express as px
from pyproj import Transformer
import pandas as pd
import numpy as np
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# functie om te testen op NaN
def isNaN(num):
    return num != num


# Functie om pivot table te maken
def pivoting(dataframe, index, column, value, fct):
    p1 = pd.pivot_table(dataframe,
                        values=value,
                        index=[index],
                        columns=[column],
                        aggfunc=fct,
                        fill_value=0,
                        margins=True,
                        margins_name='Totaal')

    p2 = p1.reset_index()

    return p2


# parameters

datafile = "data/outputVT1849 extended.csv"
beroepenfile = "data/Beroepshierarchie.csv"

footer = "Universiteit Leiden, Digital Humanities"
message = "Zicht op de volkstellingcijfers van 1849 op basis van het register van Erfgoed Leiden en Omstreken " \
          "(archiefnr. 0516-1118)"

# Read data
df = pd.read_csv(datafile,
                 usecols=["REC_ID", "WIJKNR", "STRAAT", "HUISNR", "SOORT_PERCEEL", "LON", "LAT", "HUURWAARDE",
                          "TOTINW_PERCEEL", "TYPE_REC", "SOORT_HUISHOUDEN", "TOTINW_HH", "NAAM", "LEEFTIJD",
                          "RELIGIE", "BEROEPSGROEP", "BEROEP", "BEROEPSSECTOR", "KINDEREN", "DIENSTBODES",
                          "DIENSTPERS", "STUDENTEN", "SOC_KLASSE", "SOC_KLASSE2"
                          ],
                 header=0,
                 skipinitialspace=False, delimiter=";", encoding="ISO-8859-1", low_memory=False)

# correcties, NaN geeft problemen 
df['RELIGIE'] = df['RELIGIE'].fillna('Niet Bekend')
df['SOC_KLASSE2'] = df['SOC_KLASSE2'].fillna('Niet Bekend')
df['TOTINW_PERCEEL'] = pd.to_numeric(df['TOTINW_PERCEEL'], errors='coerce')
df['TOTINW_PERCEEL'] = df['TOTINW_PERCEEL'].fillna(0)

# variables
themas = ["Personen", "Gezinnen", "Percelen", "Universiteit"]
categories = {"Percelen": ["Bewoond", "Onbewoond", "Wijken"],
              "Personen": ["Beroep", "Religie", "Sociale klasse"],
              "Gezinnen": ["Type gezin", "Religie", "Sociale klasse"],
              "Universiteit": ['Beroep']
              }
measures = {"Bewoond": ["Aantal", "Personen", "Gem. huurwaarde (fl.)"],
            "Onbewoond": ["Aantal", "Gem. huurwaarde (fl.)"],
            "Wijken": ["Aantal"],
            "Type gezin": ["Personen", "Aantal gezinnen", "Aantal kinderen", "Aantal personeel"],
            "Religie": ["Aantal"],
            "Sociale klasse": ["Aantal"],
            "Beroep": ["Aantal personen", "Gem. leeftijd"]
            }

# aparte beroepenfile
df_beroepen = pd.read_csv(beroepenfile, skipinitialspace=False, delimiter=";", encoding="ISO-8859-1")

# ******************************************************************** define application
if os.name == "nt":
    app = dash.Dash(__name__,
                external_stylesheets=[external_stylesheets],
                )
else:
    app = dash.Dash(__name__,
                external_stylesheets=[external_stylesheets],
                requests_pathname_prefix='/dashboardleiden1848/dashboard/'
                )

server = app.server
# ******************************************************************** define layout
app.layout = dash.html.Div([
    dash.html.Div([
        # -------------------  header
        dash.html.Div([dash.html.Div([
            dash.html.H4(["Dashboard Leiden 1848"],
                         style={'width': '50%',
                                'heighth': '14',
                                'display': 'inline-block'},
                         className="four columns"),
            dash.html.Textarea(
                message,
                style={'align': 'right',
                       'height': '12',
                       'display': 'inline-block'},
                className="four columns"
            ),
        ]),
        ],
            className="row pretty_container",
        ),
        # -------------------  dropdown area
        dash.html.Div([
            dash.html.H6("Thema:"),
            dash.dcc.Dropdown(
                id='selectthema',
                options=[{'label': i, 'value': i} for i in themas],
            ),
            dash.html.H6("Categorie:"),
            dash.dcc.Dropdown(
                id='selectcategory',
            ),
            dash.html.H6("Meeteenheid:"),
            dash.dcc.Dropdown(
                id='selectmeasure',
            ),
        ],
            style={'width': '25%', "margin-right": "5%", 'display': 'inline-block'},
            className="two columns pretty_container"
        ),
        # ------------------   map area
        dash.html.Div([
            dash.dcc.Graph(id='map',
                           style={'width': '100%', 'height': '800', 'display': 'inline-block'},
                           ),
        ], className="eight columns",
        ),
        # ------------------   table area
        dash.html.Div([
            dash.dash_table.DataTable(
                id='table_container',
                style_table={'height': '400px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'center',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'minWidth': '50px', 'width': '60px',
                            'maxWidth': '200px',
                            },
                style_data_conditional=[
                    {'if': {'column_id': 'Totaal'},
                     'fontWeight': 'bold',
                     },
                ],
                style_header={'textAlign': 'center',
                              'backgroundColor': 'darkblue',
                              'color': ' white',
                              'fontWeight': 'bold'
                              },
                fixed_rows={'headers': True,
                            'data': 0
                            },
                fixed_columns={'headers': True,
                               'data': 0
                               },
                tooltip_duration=None,
            ),
        ],
            style={'width': '48%'},
            className="four columns pretty_container",
        ),
        # --------------------------   graph area
        dash.html.Div([
            dash.dcc.Graph(id='plots',
                           ),
        ],
            style={'width': '48%', 'height': '200', 'display': 'inline-block'},
            className="four columns pretty_container",
        ),
    ], className="row pretty_container",
    ),
    # --------------------------   footer
    dash.html.Div([
        dash.html.P(footer,
                    style={"font-size": "10px"}
                    ),
    ],
        className="footer",
    ),
])


# ******************************************************************** CALLBACKS

# dropdown for themes
@app.callback(
    dash.Output('selectthema', 'value'),
    dash.Input('selectthema', 'options'))
def select_thema(options):
    return options[0]['value']


# dropdown for categories
@app.callback(
    dash.Output('selectcategory', 'options'),
    dash.Input('selectthema', 'value'))
def select_category_options(value):
    options = [{'label': i, 'value': i} for i in categories[value]]
    return options


@app.callback(
    dash.Output('selectcategory', 'value'),
    dash.Input('selectcategory', 'options'))
def select_category(options):
    return options[0]['value']


# dropdown for measurements
@app.callback(
    dash.Output('selectmeasure', 'options'),
    dash.Input('selectcategory', 'value'))
def select_measure_options(value):
    options = [{'label': i, 'value': i} for i in measures[value]]
    return options


@app.callback(
    dash.Output('selectmeasure', 'value'),
    dash.Input('selectmeasure', 'options'))
def select_measure(options):
    return options[0]['value']


# display graph, table, map
@app.callback(
    dash.Output('plots', 'figure'),
    dash.Output('map', 'figure'),
    dash.Output('table_container', 'columns'),
    dash.Output('table_container', 'data'),
    dash.Input('selectthema', 'value'),
    dash.Input('selectcategory', 'value'),
    dash.Input('selectmeasure', 'value'))
def show_figure(thema, category, measure):
    # ******************************************************************** DATA
    # filter the data
    if thema == "Percelen":
        if category == "Onbewoond":
            df_filter = df[df.TYPE_REC == "Onbewoond"]
        elif category == "Bewoond":
            df_filter = df[df.TYPE_REC == "hoofdhh"]
        else:  # alle percelen
            df_filter = df[(df.TYPE_REC == "hoofdhh") | (df.TYPE_REC == "Onbewoond")]
    elif thema == "Gezinnen":
        df_filter = df[(df.TYPE_REC == "hoofdhh") | (df.TYPE_REC == "nevenhh")]
    elif thema == "Personen":
        df_filter = df[df.TYPE_REC == "persoon"]
    elif thema == "Universiteit":
        df_filter = df[(df.TYPE_REC == "persoon") &
                       (~pd.isnull(df.BEROEPSGROEP)) &
                       ((df.BEROEPSGROEP == 'Universiteit') | (df.BEROEP.str.contains("student")))]
    else:
        df_filter = df

    # add column with value 1 for counting
    df_filter.loc[:, ['AANTAL']] = [1 for i in range(len(df_filter))]
    df_filter.loc[:, ['PERSONEEL']] = df_filter.DIENSTBODES + df_filter.DIENSTPERS

    # calculate measures    
    if measure == "Personen" and thema == 'Percelen':
        meetwaarden = df_filter.TOTINW_PERCEEL
        measure_column = 'TOTINW_PERCEEL'
    elif measure == "Personen" and thema != 'Percelen':
        meetwaarden = df_filter.TOTINW_HH
        measure_column = 'TOTINW_HH'
    elif measure == "Gem. huurwaarde (fl.)":
        meetwaarden = df_filter.HUURWAARDE
        measure_column = 'HUURWAARDE'
    elif measure == "Aantal personeel":
        meetwaarden = df_filter.PERSONEEL
        measure_column = 'PERSONEEL'
    elif measure == "Aantal kinderen":
        meetwaarden = df_filter.PERSONEEL
        measure_column = 'KINDEREN'
    elif measure == "Gem. leeftijd":
        meetwaarden = df_filter.LEEFTIJD
        measure_column = 'LEEFTIJD'
    else:
        meetwaarden = df_filter.AANTAL
        measure_column = 'AANTAL'

    # select data for categories 
    if category == "Type gezin":
        cat_data = "SOORT_HUISHOUDEN"
    elif category == 'Religie':
        cat_data = "RELIGIE"
    elif category == 'Sociale klasse':
        cat_data = "SOC_KLASSE2"
    elif thema == "Percelen" and category != "Wijken":
        cat_data = "SOORT_PERCEEL"
    elif thema == "Universiteit" and category == 'Beroep':
        cat_data = "BEROEP"
    elif category == "Beroep" and not thema == "Universiteit":
        cat_data = "BEROEPSGROEP"
    else:
        cat_data = "WIJKNR"

    # ******************************************************************************* MAP

    # calculte latitudes and longitudes for the map
    long = df_filter.LON
    lati = df_filter.LAT
    # input spatial system
    TRAN_28992_TO_4326 = Transformer.from_crs("EPSG:28992", "EPSG:4326")
    lat, lon = TRAN_28992_TO_4326.transform(long, lati)

    hoverdata = ["WIJKNR", "STRAAT", "HUISNR"]  # default
    hovername = "NAAM"  # default

    # calculate content for map 
    if category == "Type gezin":
        if measure == 'Gezinnen':
            hoverdata = ["WIJKNR", "STRAAT", "HUISNR", "SOORT_HUISHOUDEN"]
        elif measure == 'personen':
            hoverdata = ["WIJKNR", "STRAAT", "HUISNR", "SOORT_HUISHOUDEN", "LEEFTIJD"]
    elif thema == 'Percelen':
        hovername = "SOORT_PERCEEL"
        hoverdata = ["WIJKNR", "STRAAT", "HUISNR", "SOORT_PERCEEL", "HUURWAARDE"]
    elif thema == 'Universiteit':
        hoverdata = ["BEROEP", "LEEFTIJD", "WIJKNR", "STRAAT", "HUISNR"]
    elif category == 'Beroep':
        if measure == 'Gem. leeftijd':
            hoverdata = ["BEROEPSSECTOR", "BEROEPSGROEP", "BEROEP", "WIJKNR", "STRAAT", "HUISNR", "LEEFTIJD"]
        else:
            hoverdata = ["BEROEPSSECTOR", "BEROEPSGROEP", "BEROEP", "WIJKNR", "STRAAT", "HUISNR"]
    elif category == 'Sociale klasse':
        hoverdata = ["WIJKNR", "STRAAT", "HUISNR", "SOORT_HUISHOUDEN", "SOC_KLASSE2"]

    # draw
    mapfig = px.scatter_mapbox(df_filter,
                               lat=lat,
                               lon=lon,
                               hover_name=hovername,
                               hover_data=hoverdata,
                               color=cat_data,
                               color_continuous_scale=px.colors.cyclical.IceFire,
                               zoom=14,
                               height=400)

    # mapfig.update_layout(mapbox_style="open-street-map") # switch voor maken?
    mapfig.update_layout(mapbox_style="carto-positron")

    mapfig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                         mapbox=dict(
                             bearing=0,
                             center=go.layout.mapbox.Center(
                                 lat=52.1587,  # centre coord Leiden
                                 lon=4.4933
                             ),
                             pitch=0,
                             zoom=14
                         )
                         )
    # ************************************************************************************ GRAPH

    if category == 'Beroep':

        # Group by  for sunburst chart
        if (category == "Beroep") and (not thema == "Universiteit"):
            # group by in the filtered df beroepssector and beroepsgroep
            filter_length = len(df_filter)
            arrays = [df_filter.BEROEPSGROEP, df_filter.BEROEPSSECTOR]
            index = pd.MultiIndex.from_arrays(arrays, names=('BEROEPSSECTOR', 'BEROEPSGROEP'))
            df_extract = pd.DataFrame({'COUNT': [1 for i in range(filter_length)]}, index=index)
            df_aggregate = df_extract.groupby(level=['BEROEPSGROEP', "BEROEPSSECTOR"]).sum()

        elif (category == "Beroep") and (thema == "Universiteit"):
            # group by df_filter at beroepssector and beroepsgroep
            filter_length = len(df_filter)
            arrays = [df_filter.BEROEP, df_filter.BEROEPSGROEP]
            index = pd.MultiIndex.from_arrays(arrays, names=('BEROEP', 'BEROEPSGROEP'))
            df_extract = pd.DataFrame({'COUNT': [1 for i in range(filter_length)]}, index=index)
            if measure == 'Gem. leeftijd':
                df_aggregate = df_extract.groupby(level=['BEROEP', "BEROEPSGROEP"]).mean()
            else:
                df_aggregate = df_extract.groupby(level=['BEROEP', "BEROEPSGROEP"]).sum()
            df_sun = df_aggregate.reset_index(
                level=['BEROEPSGROEP', 'BEROEP'])  # put grouplevels back from index to frame

        # plot sunburst chart

        fig = go.Figure()

        if thema == "Universiteit":
            # make lists for sunburst
            unique_groepen = list(set(df_sun.BEROEPSGROEP))
            ids = unique_groepen + list(df_sun.BEROEP)
            # calculate values
            tel = [0 for j in unique_groepen]
            for i in range(len(df_sun.BEROEPSGROEP)):
                for j in range(len(unique_groepen)):
                    if df_sun.BEROEPSGROEP[i] == unique_groepen[j]:
                        tel[j] = list(df_sun.COUNT)[i] + tel[j]
            values = tel + list(df_sun.COUNT)

            fig.add_trace(go.Sunburst(ids=ids,
                                      labels=ids,
                                      parents=['' for i in unique_groepen] + list(df_sun.BEROEPSGROEP),
                                      values=values,
                                      ))

            fig.update_layout(margin=dict(t=20, l=0, r=0, b=0),
                              title_text=category + " - " + measure,
                              title_font_size=12
                              )

        else:  # beroepen
            fig.add_trace(go.Sunburst(
                ids=df_beroepen.BEROEPSGROEP,
                labels=df_beroepen.BEROEP_LABEL,
                parents=df_beroepen.BEROEPSSECTOR,
                values=df_aggregate.COUNT,
                domain=dict(column=0)
            )
            )

            fig.update_layout(margin=dict(t=20, l=0, r=0, b=0),
                              title_text=category + " - " + measure,
                              title_font_size=12,
                              )

    else:
        # Piechart
        # labels for graph

        pielabels = df_filter[cat_data]

        # plot piechart
        fig = go.Figure(data=[go.Pie(labels=pielabels,
                                     values=meetwaarden,
                                     )
                              ])
        fig.update_traces(textposition='inside',
                          hoverinfo='label+percent',
                          textinfo='value',
                          marker=dict(line=dict(color='#000000', width=1))
                          )
        fig.update_layout(title_text=category + " - " + measure,
                          overwrite=True,
                          title_font_size=14,
                          uniformtext_minsize=10,
                          uniformtext_mode='hide')

    # ******************************************************************** TABLE
    if category == 'Wijken':
        cat_data = "SOORT_PERCEEL"

    # calculate pivot table
    if measure == 'Gem. leeftijd' or measure == 'Gem. huurwaarde (fl.)':
        table = pivoting(df_filter, cat_data, 'WIJKNR', measure_column, np.mean)
        table = table.round(1)
    else:
        table = pivoting(df_filter, cat_data, 'WIJKNR', measure_column, np.sum)
    # rename indez last row
    table = table.rename(index={table.index[len(table) - 1]: "Totaal"})

    # from table calculate columns and data for callback
    column_type = ['text', 'numeric', 'numeric', 'numeric', 'numeric', 'numeric', 'numeric', 'numeric', 'numeric',
                   'numeric', 'numeric']
    add = ['', "Wijk ", "Wijk ", "Wijk ", "Wijk ", "Wijk ", "Wijk ", "Wijk ", "Wijk ", '']
    columns = [{"name": add[i] + str(table.columns[i]), "id": str(table.columns[i]), 'type': column_type[i]}
               for i in range(len(table.columns))]
    data = table.to_dict('records')

    # ********************************** end CALLBACK
    return fig, mapfig, columns, data


# *******************************************************************************application
if __name__ == '__main__':
         if os.name == "nt":
             app.run_server(port=8051, debug=False) # local
         else:
             app.run_server(debug=False)  # server
