#
# Imports
#
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import configparser
import os

from Plugins.globals import mapbox_token
from Plugins.Data import exceldata as data
from Plugins.helpers import get_variables, merge_years

#
# Country heat map
#
def create_country_map(min_year, max_year):
    merged_df = data.birthcountry_df[data.birthcountry_df['year'] <= max_year]
    merged_df = merged_df[merged_df['year'] >= min_year]
    merged_df = merged_df[['country', 'count', 'iso_alpha', 'lat', 'lon']]
    filtered_df = merged_df.groupby(merged_df['country']).aggregate({'count': 'sum', 'iso_alpha': 'first'})
    filtered_df = filtered_df.reset_index()
    filtered_df: object = filtered_df.sort_values(by=['count', 'country'], ascending=False)
    fig = px.choropleth(filtered_df, locations='iso_alpha', color='count', hover_name='country',
                        color_continuous_scale='plasma', labels={'count': 'Number of appointments'},
                        )
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      margin=dict(l=0, r=0, t=0, b=0), modebar_orientation='v',)
    fig.update_geos(
        visible=True, resolution=110,
        showcountries=True, countrycolor="black"
    )
    return fig, filtered_df

#
# Country line map
#
def create_country_line_map(min_year, max_year):
    merged_df = data.birthcountry_df[data.birthcountry_df['year'] <= max_year]
    merged_df = merged_df[merged_df['year'] >= min_year]
    merged_df = merged_df[['country', 'count', 'iso_alpha', 'lat', 'lon']]
    filtered_df = merged_df.groupby(merged_df['country']).aggregate(
        {'count': 'sum', 'iso_alpha': 'first', 'lat': 'first', 'lon': 'first'})
    filtered_df = filtered_df.reset_index()
    filtered_df = filtered_df.sort_values(by=['count', 'country'], ascending=False)
    fig = px.scatter_geo(filtered_df, locations='iso_alpha', color='country', size='count')
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      margin=dict(l=0, r=0, t=0, b=0), modebar_orientation='v',)
    fig.update_geos(
        visible=True, resolution=110,
        showcountries=True, countrycolor="black"
    )
    lats = np.empty(3 * len(filtered_df))
    lats[::3] = filtered_df['lat']
    lats[1::3] = 52.160114
    lats[2::3] = None
    lons = np.empty(3 * len(filtered_df))
    lons[::3] = filtered_df['lon']
    lons[1::3] = 4.497010
    lons[2::3] = None
    fig.add_trace(
        go.Scattergeo(
            lat=lats,
            lon=lons,
            mode='lines',
            line=dict(width=1, color='blue'),
            name='Place of birth'
        )
    )
    return fig, filtered_df

#
# Country animated heat map
#
def create_animated_country_map(min_year, max_year):
    merged_df = data.birthcountry_df[data.birthcountry_df['year'] <= max_year]
    merged_df = merged_df[merged_df['year'] >= min_year]
    fig = px.choropleth(merged_df, locations='iso_alpha', color='count', hover_name='country', animation_frame='year',
                        color_continuous_scale='plasma', labels={'count': 'Number of appointments'})
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      margin=dict(l=0, r=0, t=0, b=0), modebar_orientation='v',)
    return fig, merged_df

#
# Country mapbox heat map
#
def create_mapbox_heat_map(min_year, max_year):
    # from urllib.request import urlopen
    import json
    with open(os.environ['PLUGINS_BASEPATH']+'assets/countries.geojson') as response:
        countries = json.load(response)

    merged_df = data.birthcountry_df[data.birthcountry_df['year'] <= max_year]
    merged_df = merged_df[merged_df['year'] >= min_year]
    max_value = merged_df['count'].max()

    fig = px.choropleth_mapbox(
        data_frame=merged_df,
        geojson=countries,
        locations='iso_alpha',
        color='count',
        color_continuous_scale='plasma',
        range_color=(0, max_value),
        featureidkey='properties.ISO_A3',
        mapbox_style='carto-positron',
        center={"lat": 52, "lon": -5},
        zoom=1,
        animation_frame='century',
        labels={'count': 'Number of appointments'},
    )

    fig.update_layout(
        paper_bgcolor='rgba(223,223,218,0.7)',
        font_color='black',
        margin=dict(l=0, r=0, t=30, b=0),
        hoverlabel_align='right',
        modebar_orientation='v',
    )

    return fig, merged_df

#
# Country mapbox scatter map
#
def create_mapbox_scatter_map(min_year, max_year):
    merged_df = data.birthcountry_df[data.birthcountry_df['year'] <= max_year]
    merged_df = merged_df[merged_df['year'] >= min_year]
    merged_df['color'] = merged_df['count'].fillna(0).replace(np.inf, 0)
    years = merged_df['year'].unique()
    frames = [{
        'name': 'frame_{}'.format(year),
        'data': [{
            'type': 'scattermapbox',
            'lat': merged_df.loc[merged_df['year'] == year, 'lat'],
            'lon': merged_df.loc[merged_df['year'] == year, 'lon'],
            'marker': go.scattermapbox.Marker(
                size=merged_df.loc[merged_df['year'] == year, 'count'] /
                    merged_df.loc[merged_df['year'] == year, 'count'].max() * 100,
                color=merged_df.loc[merged_df['year'] == year, 'count'] /
                    merged_df.loc[merged_df['year'] == year, 'count'].max() * 100,
                showscale=True,
                colorbar={'title': 'Appointments', 'titleside': 'top', 'thickness': 20, 'ticksuffix': ' %'},
            ),
            'customdata': np.stack((merged_df.loc[merged_df['year'] == year, 'country'],
                                    merged_df.loc[merged_df['year'] == year, 'count'],
                                    merged_df.loc[merged_df['year'] == year, 'iso_alpha']), axis=-1),
            'hovertemplate': "<extra></extra><em>%{customdata[0]}  </em><br> %{customdata[1]}<br> %{customdata[2]}<br>",
        }],
    } for year in years]

    sliders = [{
        'transition': {'duration': 0},
        'x': 0.08,
        'len': 0.88,
        'currentvalue': {'font': {'size': 15}, 'prefix': '📅 ', 'visible': True, 'xanchor': 'center'},
        'steps': [
            {
                'label': str(year),
                'method': 'animate',
                'args': [
                    ['frame_{}'.format(year)],
                    {'mode': 'immediate', 'frame': {'duration': 600, 'redraw': True}, 'transition': {'duration': 120}}
                ],
            } for year in years]
    }]

    layout = go.Layout(
        sliders=sliders,
        updatemenus=[{
            'type': 'buttons',
            'showactive': True,
            'x': 0.045, 'y': -0.08,
            'buttons': [{
                'label': '▶️',
                'method': 'animate',
                'args': [
                    None,
                    {
                        'frame': {'duration': 600, 'redraw': True},
                        'transition': {'duration': 120},
                        'fromcurrent': True,
                        'mode': 'immediate',
                    }
                ]
            }]
        }],
        mapbox={
            'accesstoken': mapbox_token,
            'center': {"lat": 52, "lon": -5},
            'zoom': 1,
            'style': 'light',
        },
    )

    figure_data = frames[0]['data']

    fig = go.Figure(data=figure_data, layout=layout, frames=frames)

    fig.update_layout(
        paper_bgcolor='rgba(223,223,218,0.7)',
        font_color='black',
        margin=dict(l=0, r=0, t=0, b=40),
        showlegend=False,
        hoverlabel_align='right',
        modebar_orientation='v',
    )
    return fig, merged_df


#
# individual map
#
def create_map(city, country, birthyear):
    # TODO: add coordination to cities
    origin_country = \
        data.birthcountry_df.loc[data.birthcountry_df['country'] == country,
                                 ['country', 'iso_alpha', 'lat', 'lon']].iloc[0]
    origin = pd.DataFrame(origin_country)
    countries = origin.T
    countries = countries.concat({'country': 'Nederland', 'iso_alpha': 'NLD', 'lat': '52.21158', 'lon': '5.600489'},
                                 ignore_index=True)
    places = origin.T
    places = places.rename(columns={'country': 'city'})
    places = places.concat({'city': 'Leiden', 'iso_alpha': 'NLD', 'lat': '52.15833', 'lon': '4.49306'},
                           ignore_index=True)
    fig = px.choropleth(countries, locations='iso_alpha', hover_name='country', color='iso_alpha',
                        color_continuous_scale='plasma', labels={'iso_alpha': 'Places'})
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      margin=dict(l=0, r=0, t=15, b=0), modebar_orientation='h',)
    fig.add_trace(go.Scattergeo(
        locationmode='ISO-3',
        lat=places['lat'],
        lon=places['lon'],
        hoverinfo='text',
        text=places['city'],
        mode='markers',
        marker=dict(
            size=10,
            color='rgb(255, 0, 0)',
            line=dict(
                width=3,
                color='rgba(68, 68, 68, 0)'
            )
        )
    ))
    fig.add_trace(go.Scattergeo(
        locationmode='ISO-3',
        lat=[places['lat'][0], places['lat'][1]],
        lon=[places['lon'][0], places['lon'][1]],
        mode='lines',
        line=dict(width=5, color='red'),
    ))
    return fig
