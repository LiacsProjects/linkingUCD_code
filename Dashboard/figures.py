# Creating dataframe
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import data



# Create figures
def get_variables(subject):
    if subject == 'Number of enrollments':
        selected_df = data.year_df
        subjectx = 'year'
        name = 'Number of enrollments'
    elif subject == 'Origin countries':
        selected_df = data.country_df
        subjectx = 'country'
        name = 'Country'
    elif subject == 'Origin cities':
        selected_df = data.city_df
        subjectx = 'city'
        name = 'City'
    elif subject == 'Origin regions':
        selected_df = data.region_df
        subjectx = 'region'
        name = 'Region'
    elif subject == 'Enrollment ages':
        selected_df = data.age_df
        subjectx = 'age'
        name = 'Age'
    elif subject == 'Enrollment faculties':
        selected_df = data.fac_df
        subjectx = 'faculty'
        name = 'Faculty'
    elif subject == 'Royal status':
        selected_df = data.status_df
        subjectx = 'status'
        name = 'Status'
    elif subject == 'Student jobs':
        selected_df = data.job_df
        subjectx = 'job'
        name = 'Job'
    elif subject == 'Student religion':
        selected_df = data.rel_df
        subjectx = 'religion'
        name = 'Religion'
    else:
        selected_df = data.year_df
        subjectx = 'year'
        name = 'Number of enrollments'
    return selected_df, subjectx, name


def merge_years(df, subject):
    all_centuries = pd.DataFrame()
    for cent in df.century.unique():
        current_century = df[df.century == cent]
        if subject != 'year' and subject == 'country':
            trimmed_century = current_century[[subject, 'count', 'century', 'iso_alpha']]
        elif subject != 'year':
            trimmed_century = current_century[[subject, 'count', 'century']]
        else:
            trimmed_century = current_century
        if subject != 'country':
            new_century = trimmed_century.groupby(trimmed_century[subject]).aggregate(
                {subject: 'first', 'count': 'sum', 'century': 'first'})
        else:
            new_century = trimmed_century.groupby(trimmed_century[subject]).aggregate(
                {subject: 'first', 'count': 'sum', 'century': 'first', 'iso_alpha': 'first'})
        if subject != 'age':
            new_century = new_century.sort_values(by=['count'], ascending=False)
        all_centuries = pd.concat([all_centuries, new_century], axis=0)
    all_centuries.reset_index(inplace=True, drop=True)
    return all_centuries


# Yearly graph
def create_year_cent_figure(subject, century, year, age, mode):
    selected_df, subjectx, name = get_variables(subject)
    filtered_df = selected_df[selected_df['century'] <= century[1]]
    filtered_df = filtered_df[filtered_df['century'] >= century[0]]
    filtered_df = filtered_df[filtered_df['year'] <= year[1]]
    filtered_df = filtered_df[filtered_df['year'] >= year[0]]
    if subjectx == 'age':
        filtered_df = filtered_df[filtered_df['age'] <= int(age[1])]
        filtered_df = filtered_df[filtered_df['age'] >= int(age[0])]
        filtered_df = filtered_df.sort_values(by=['year', subjectx, 'century'], ascending=True)
    if mode == 'Line graph':
        fig = px.line(filtered_df, x='year', y='count', color=subjectx, markers=True,
                      labels={subjectx: name, 'count': 'Number of enrollments', 'year': 'Year', 'century': 'Century'},
                      hover_name=subjectx, hover_data=['year', 'century'])
    elif mode == 'Scatter graph':
        fig = px.scatter(filtered_df, x='year', y='count', size='count', color=subjectx, color_continuous_scale='blues',
                         log_x=True, labels={subjectx: name, 'count': 'Number of enrollments', 'year': 'Year', 'century': 'Century'},
                         hover_name=subjectx, hover_data=['year', 'century'])
    elif mode == 'Bar graph':
        fig = px.bar(filtered_df, x='year', y='count', color=subjectx, color_continuous_scale='blues',
                     labels={subjectx: name, 'count': 'Number of enrollments', 'year': 'Year', 'century': 'Century'},
                     hover_name=subjectx, hover_data=['year', 'century'])
    if subjectx == 'year':
        title_cent = name + ' per year in the '
    else:
        title_cent = 'Number of enrollments per ' + name + ' per year in the '
    if century[0] == century[1]:
        title_cent += (str(century[0]) + 'th century ')
    else:
        title_cent += (str(century[0]) + 'th' + '-' + str(century[1]) + 'th century')
    if mode == 'Bar graph':
        fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                          title=title_cent)
    else:
        fig.update_traces(mode='markers+lines')
        fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                          title=title_cent)
    fig.update_xaxes(type='category')
    return fig


# Century graph
def create_cent_figure(subject, century):
    selected_df, subjectx, name = get_variables(subject)
    merged_df = merge_years(selected_df, subjectx)
    filtered_df = merged_df[merged_df['century'] <= century[1]]
    filtered_df = filtered_df[filtered_df['century'] >= century[0]]
    if subjectx == 'year' or subjectx == 'age':
        filtered_df = filtered_df.sort_values(by=[subjectx, 'century'], ascending=True)
    else:
        filtered_df = filtered_df.sort_values(by=['count', 'century'], ascending=False)
    fig = px.bar(filtered_df, x=subjectx, y='count', color=subjectx, color_continuous_scale='blues',
                 hover_name=subjectx, hover_data=['century'], labels={subjectx: name, 'count': 'Number of enrollments', 'year': 'Year', 'century': 'Century'})
    if subjectx == 'year':
        title_cent = name + ' in the '
    else:
        title_cent = 'Number of enrollments per ' + name + ' in the '
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
                 hover_name=subjectx, labels={'century': 'Century', 'count': 'Number of enrollments'})
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      title=name + ' per century')
    fig.update_xaxes(type='category')
    return fig


# subject information table
def create_century_table(df, name):
    table_df = pd.DataFrame(columns=['Statistic', 'Enrollments'])
    for cent in df['century'].unique():
        table_df.loc[len(table_df)] = ['Century', cent]
        table_df.loc[len(table_df)] = ['Total enrollments', df.loc[df['century'] == cent, 'count'].sum().round(0)]
        table_df.loc[len(table_df)] = ['Average enrollments', df.loc[df['century'] == cent, 'count'].mean().round(0)]
        table_df.loc[len(table_df)] = ['Most enrollments',
                                       df.loc[df['century'] == cent].sort_values(by='count', ascending=False).iloc[0][0]]
        table_df.loc[len(table_df)] = ['Least enrollments',
                                       df.loc[df['century'] == cent].sort_values(by='count', ascending=False).iloc[0][0]]
    return table_df


# Country heat map
def create_country_map(min_year, max_year):
    merged_df = data.country_df[data.country_df['year'] <= max_year]
    merged_df = merged_df[merged_df['year'] >= min_year]
    merged_df = merged_df[['country', 'count', 'iso_alpha', 'lat', 'lon']]
    filtered_df = merged_df.groupby(merged_df['country']).aggregate({'count': 'sum', 'iso_alpha': 'first'})
    filtered_df = filtered_df.reset_index()
    filtered_df = filtered_df.sort_values(by=['count', 'country'], ascending=False)
    fig = px.choropleth(filtered_df, locations='iso_alpha', color='count', hover_name='country',
                                  color_continuous_scale='plasma', labels={'count': 'Number of enrollments'})
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                                title='Student enrollments per country')
    return fig, filtered_df


# Country line map
def create_country_line_map(min_year, max_year):
    merged_df = data.country_df[data.country_df['year'] <= max_year]
    merged_df = merged_df[merged_df['year'] >= min_year]
    merged_df = merged_df[['country', 'count', 'iso_alpha', 'lat', 'lon']]
    filtered_df = merged_df.groupby(merged_df['country']).aggregate({'count': 'sum', 'iso_alpha': 'first', 'lat': 'first', 'lon': 'first'})
    filtered_df = filtered_df.reset_index()
    filtered_df = filtered_df.sort_values(by=['count', 'country'], ascending=False)
    fig = px.scatter_geo(filtered_df, locations='iso_alpha', color='country', size='count')
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      title='Student enrollments per country')
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
            name='Birth Country to Leiden'
        )
    )
    return fig, filtered_df


# individual map
def create_map(city, country, birthyear, age):
    print(city)
    print(country)
    print(birthyear)
    print(age)
    df = data.country_df
    place = df.loc[df['country'] == country]
    print(place)
    info = pd.DataFrame(place.iloc[0]).T
    print(info)
    fig = px.choropleth(info, locations='iso_alpha', color='country', color_continuous_scale='plasma')
    return fig



# Individual chart information
def get_unique_values(subject):
    unique_values = data.individual_df[subject].unique()
    unique_values = unique_values.tolist()
    unique_values.remove('?')
    return unique_values


def remove_nan(subject):
    unique_values = data.individual_df[subject].unique()
    unique_values = unique_values[1:]
    return unique_values
