# Creating dataframe
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import data
import configparser
import os

config = configparser.ConfigParser()
config.read(os.environ['DASHBOARD_BASEPATH'] + 'assets/config.ini')
mapbox_token = config['mapbox']['token']


# Create figures
def get_variables(subject):
    if subject == 'Gender':
        selected_df = data.gender_df
        subjectx = 'gender'
        name = 'Gender'
    if subject == 'Title':
        selected_df = data.title_df
        subjectx = 'title'
        name = 'Title'
    if subject == 'Birth':
        selected_df = data.birth_df
        subjectx = 'birth'
        name = 'Birth'
    if subject == 'Birth place':
        selected_df = data.birthplace_df
        subjectx = 'birth place'
        name = 'Birth place'
    if subject == 'Birth country':
        selected_df = data.birthcountry_df
        subjectx = 'country'
        name = 'Birth country'
    if subject == 'Death':
        selected_df = data.death_df
        subjectx = 'death'
        name = 'Death'
    if subject == 'Death place':
        selected_df = data.deathplace_df
        subjectx = 'death place'
        name = 'Death place'
    if subject == 'Death country':
        selected_df = data.deathcountry_df
        subjectx = 'country'
        name = 'Death country'
    if subject == 'Promotion':
        selected_df = data.promotion_df
        subjectx = 'promotion'
        name = 'Promotion'
    if subject == 'Promotion type':
        selected_df = data.promotiontype_df
        subjectx = 'promotion type'
        name = 'Promotion type'
    if subject == 'Promotion place':
        selected_df = data.promotion_place_df
        subjectx = 'promotion place'
        name = 'Promotion place'
    if subject == 'Appointment':
        selected_df = data.appointment_df
        subjectx = 'appointment'
        name = 'Appointment'
    if subject == 'Job':
        selected_df = data.professor_job_df
        subjectx = 'job'
        name = 'Job'
    if subject == 'Subject area':
        selected_df = data.subject_df
        subjectx = 'subject area'
        name = 'Subject area'
    if subject == 'Faculty':
        selected_df = data.faculty_df
        subjectx = 'faculty'
        name = 'Faculty'
    if subject == 'End of employment':
        selected_df = data.end_df
        subjectx = 'end of employment'
        name = 'End of employment'
    return selected_df, subjectx, name


def merge_years(df, subject):
    all_centuries = pd.DataFrame()
    for cent in df.century.unique():
        current_century = df[df.century == cent]
        trimmed_century = current_century[[subject, 'count', 'century']]
        new_century = trimmed_century.groupby(trimmed_century[subject]).aggregate(
            {subject: 'first', 'count': 'sum', 'century': 'first'})
        all_centuries = pd.concat([all_centuries, new_century], axis=0)
    all_centuries.reset_index(inplace=True, drop=True)
    return all_centuries


# Yearly graph
def create_year_cent_figure(subject, century, year, mode):
    selected_df, subjectx, name = get_variables(subject)
    filtered_df = selected_df[selected_df['century'] <= century[1]]
    filtered_df = filtered_df[filtered_df['century'] >= century[0]]
    filtered_df = filtered_df[filtered_df['year'] <= year[1]]
    filtered_df = filtered_df[filtered_df['year'] >= year[0]]
    if mode == 'Line graph':
        fig = px.line(filtered_df, x='year', y='count', color=subjectx, markers=True,
                      labels={subjectx: name, 'count': 'Number of appointments', 'year': 'Year', 'century': 'Century'},
                      hover_name=subjectx, hover_data=['year', 'century'])
    elif mode == 'Scatter graph':
        fig = px.scatter(filtered_df, x='year', y='count', size='count', color=subjectx, color_continuous_scale='blues',
                         log_x=True, labels={subjectx: name, 'count': 'Number of appointments', 'year': 'Year',
                                             'century': 'Century'},
                         hover_name=subjectx, hover_data=['year', 'century'])
    elif mode == 'Bar graph':
        fig = px.bar(filtered_df, x='year', y='count', color=subjectx, color_continuous_scale='blues',
                     labels={subjectx: name, 'count': 'Number of appointments', 'year': 'Year', 'century': 'Century'},
                     hover_name=subjectx, hover_data=['year', 'century'])
    if subjectx == 'year':
        title_cent = name + ' per year in the '
    else:
        title_cent = 'Number of appointments per ' + name + ' per year in the '
    if century[0] == century[1]:
        title_cent += (str(century[0]) + 'th century ')
    else:
        title_cent += (str(century[0]) + 'th' + '-' + str(century[1]) + 'th century')
    if mode == 'Bar graph':
        fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black',
                          plot_bgcolor='rgba(223,223,218,0.7)',
                          title=title_cent)
    else:
        fig.update_traces(mode='markers+lines')
        fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black',
                          plot_bgcolor='rgba(223,223,218,0.7)',
                          title=title_cent)
    fig.update_xaxes(type='category')
    return fig


# Century graph
def create_cent_figure(subject, century):
    selected_df, subjectx, name = get_variables(subject)
    merged_df = merge_years(selected_df, subjectx)
    filtered_df = merged_df[merged_df['century'] <= century[1]]
    filtered_df = filtered_df[filtered_df['century'] >= century[0]]
    if subjectx == 'year':
        filtered_df = filtered_df.sort_values(by=[subjectx, 'century'], ascending=True)
    else:
        filtered_df = filtered_df.sort_values(by=['count', 'century'], ascending=False)
    fig = px.bar(filtered_df, x=subjectx, y='count', color=subjectx, color_continuous_scale='blues',
                 hover_name=subjectx, hover_data=['century'],
                 labels={subjectx: name, 'count': 'Number of appointments', 'year': 'Year', 'century': 'Century'})
    if subjectx == 'year':
        title_cent = name + ' in the '
    else:
        title_cent = 'Number of appointments per ' + name + ' in the '
    if century[0] == century[1]:
        title_cent += (str(century[0]) + 'th century')
    else:
        title_cent += (str(century[0]) + 'th' + '-' + str(century[1]) + 'th century')
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      title=title_cent)
    fig.update_xaxes(type='category')
    return fig


# Subject info graph
def create_subject_info_graph(subject):
    selected_df, subjectx, name = get_variables(subject)
    merged_df = merge_years(selected_df, subjectx)
    if subjectx == 'year' or subjectx == 'age':
        merged_df = merged_df.sort_values(by=[subjectx, 'century'], ascending=True)
    fig = px.bar(merged_df, x='century', y='count', color=subjectx, color_continuous_scale='blues',
                 hover_name=subjectx, labels={'century': 'Century', 'count': 'Number of appointments'})
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      title=name + ' per century')
    fig.update_xaxes(type='category')
    return fig


# subject information table
def create_century_table(df, name):
    table_df = pd.DataFrame(columns=['Statistic', 'appointments'])
    for cent in df['century'].unique():
        table_df.loc[len(table_df)] = ['Century', cent]
        table_df.loc[len(table_df)] = ['Total appointments', round(df.loc[df['century'] == cent, 'count'].sum(),0)]
        table_df.loc[len(table_df)] = ['Average appointments', round(df.loc[df['century'] == cent, 'count'].mean(),0)]
        table_df.loc[len(table_df)] = ['Most appointments',
                                       df.loc[df['century'] == cent].sort_values(by='count', ascending=False).iloc[0][
                                           0]]
        table_df.loc[len(table_df)] = ['Least appointments',
                                       df.loc[df['century'] == cent].sort_values(by='count', ascending=False).iloc[0][
                                           0]]
    return table_df


# Country heat map
def create_country_map(min_year, max_year):
    merged_df = data.birthcountry_df[data.birthcountry_df['year'] <= max_year]
    merged_df = merged_df[merged_df['year'] >= min_year]
    merged_df = merged_df[['country', 'count', 'iso_alpha', 'lat', 'lon']]
    filtered_df = merged_df.groupby(merged_df['country']).aggregate({'count': 'sum', 'iso_alpha': 'first'})
    filtered_df = filtered_df.reset_index()
    filtered_df = filtered_df.sort_values(by=['count', 'country'], ascending=False)
    fig = px.choropleth(filtered_df, locations='iso_alpha', color='count', hover_name='country',
                        color_continuous_scale='plasma', labels={'count': 'Number of appointments'})
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      margin=dict(l=0, r=0, t=0, b=0))
    fig.update_geos(
        visible=True, resolution=110,
        showcountries=True, countrycolor="black"
    )
    return fig, filtered_df


# Country line map
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
                      margin=dict(l=0, r=0, t=0, b=0))
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


# Country animated heat map
def create_animated_country_map(min_year, max_year):
    merged_df = data.birthcountry_df[data.birthcountry_df['year'] <= max_year]
    merged_df = merged_df[merged_df['year'] >= min_year]
    fig = px.choropleth(merged_df, locations='iso_alpha', color='count', hover_name='country', animation_frame='year',
                        color_continuous_scale='plasma', labels={'count': 'Number of appointments'})
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      margin=dict(l=0, r=0, t=0, b=0))
    return fig, merged_df


# Country mapbox heat map
def create_mapbox_heat_map(min_year, max_year):
    from urllib.request import urlopen
    import json
    with open('../assets/countries.geojson') as response:
        countries = json.load(response)
    merged_df = data.birthcountry_df[data.birthcountry_df['year'] <= max_year]
    merged_df = merged_df[merged_df['year'] >= min_year]
    max_value = merged_df['count'].max()
    fig = px.choropleth_mapbox(
        merged_df,
        geojson=countries,
        locations='iso_alpha',
        color='count',
        color_continuous_scale='plasma',
        range_color=(0, max_value),
        featureidkey='properties.ISO_A3',
        mapbox_style='carto-positron',
        center={"lat": 52, "lon": -5},
        zoom=1,
        animation_frame='year',
        labels={'count': 'Number of appointments'}
    )

    fig.update_layout(
        paper_bgcolor='rgba(223,223,218,0.7)',
        font_color='black',
        margin=dict(l=0, r=0, t=30, b=0),
        hoverlabel_align='right',
    )

    return fig, merged_df


# Country mapbox scatter map
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
    )
    return fig, merged_df


# individual map
def create_map(city, country, birthyear):
    # TODO: add coordination to cities
    origin_country = data.birthcountry_df.loc[data.birthcountry_df['country'] == country, ['country', 'iso_alpha', 'lat', 'lon']].iloc[0]
    origin = pd.DataFrame(origin_country)
    countries = origin.T
    countries = countries.append({'country': 'Nederland', 'iso_alpha':'NLD', 'lat':'52.21158', 'lon':'5.600489'}, ignore_index=True)
    places = origin.T
    places = places.rename(columns={'country': 'city'})
    places = places.append({'city': 'Leiden', 'iso_alpha': 'NLD', 'lat': '52.15833', 'lon': '4.49306'},
                           ignore_index=True)
    fig = px.choropleth(countries, locations='iso_alpha', hover_name='country', color='iso_alpha',
                        color_continuous_scale='plasma', labels={'iso_alpha': 'Places'})
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      margin=dict(l=0, r=0, t=0, b=0))
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


# Individual chart information
def get_unique_values(subject):
    unique_values = data.individual_profs_df[subject].unique()
    unique_values = unique_values.tolist()
    return unique_values


def remove_nan(subject):
    unique_values = data.individual_profs_df[subject].unique()
    unique_values = unique_values[1:]
    return unique_values
