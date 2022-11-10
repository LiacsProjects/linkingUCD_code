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
    if subject == 'Rectors':
        selected_df = data.rector_per_year
        subjectx = 'year'
        name = 'Number of rectores'
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
    if mode == 'Scatter graph':
        fig = px.line(filtered_df, x='year', y='count', color=subjectx, markers=True,
                      labels={subjectx: name, 'count': 'Number of rectors', 'year': 'Year', 'century': 'Century'},
                      hover_name=subjectx, hover_data=['year', 'century'])
    elif mode == 'Line graph':
        fig = px.scatter(filtered_df, x='year', y='count', size='count',
                         color=subjectx, color_continuous_scale='blues',
                         log_x=True, labels={subjectx: name, 'count': 'Number of rectors', 'year': 'Year',
                                             'century': 'Century'},
                         hover_name=subjectx, hover_data=['year', 'century'])
    elif mode == 'Bar graph':
        fig = px.bar(filtered_df, x='year', y='count',
                     color=subjectx, color_continuous_scale='blues',
                     labels={subjectx: name, 'count': 'Number of rectors', 'year': 'Year', 'century': 'Century'},
                     hover_name=subjectx, hover_data=['year', 'century'])
    if subjectx == 'year':
        title_cent = name + ' per year in the '
    else:
        title_cent = 'Number of rectors per ' + name + ' per year in the '
    if century[0] == century[1]:
        title_cent += (str(century[0]) + 'th century ')
    else:
        title_cent += (str(century[0]) + 'th' + '-' + str(century[1]) + 'th century')
    if mode == 'Bar graph':
        fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black',
                          plot_bgcolor='rgba(223,223,218,0.7)',
                          title=title_cent)
        #fig.update_traces(marker_color='#001158')
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
                 labels={subjectx: name, 'count': 'Number of rectors', 'year': 'Year', 'century': 'Century'})
    if subjectx == 'year':
        title_cent = name + ' in the '
    else:
        title_cent = 'Number of rectors per ' + name + ' in the '
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
                 hover_name=subjectx, labels={'century': 'Century', 'count': 'Number of rectors'})
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      title=name + ' per century')
    fig.update_xaxes(type='category')
    return fig


# subject information table
def create_century_table(df, name):
    table_df = pd.DataFrame(columns=['Statistic', 'Rectors'])
    for cent in df['century'].unique():
        table_df.loc[len(table_df)] = ['Century', cent]
        table_df.loc[len(table_df)] = ['Total rectors', df.loc[df['century'] == cent, 'count'].sum().round(0)]
        table_df.loc[len(table_df)] = ['Average rectors', df.loc[df['century'] == cent, 'count'].mean().round(0)]
        table_df.loc[len(table_df)] = ['Most rectors',
                                       df.loc[df['century'] == cent].sort_values(by='count', ascending=False).iloc[0][
                                           0]]
        table_df.loc[len(table_df)] = ['Least rectors',
                                       df.loc[df['century'] == cent].sort_values(by='count', ascending=False).iloc[0][
                                           0]]
    return table_df


# individual map
def create_map(city, country, birthyear):
    # TODO: add coordination to cities
    origin_country = data.country_df.loc[data.country_df['country'] == country, ['country', 'iso_alpha', 'lat', 'lon']].iloc[0]
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
    unique_values = data.individual_df[subject].unique()
    unique_values = unique_values.tolist()
    return unique_values


def remove_nan(subject):
    unique_values = data.individual_df[subject].unique()
    unique_values = unique_values[1:]
    return unique_values
