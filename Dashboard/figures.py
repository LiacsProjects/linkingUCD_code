# Creating dataframe
import plotly.express as px
import pandas as pd
from dash import html
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
def create_year_cent_figure(subject, century, year, age, mode, hover):
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
    title_cent = ''
    if century[0] == century[1]:
        title_cent += (str(century[0]) + 'th')
    else:
        title_cent += (str(century[0]) + 'th' + '-' + str(century[1]) + 'th')
    if mode == 'Bar graph':
        fig.update_layout(paper_bgcolor='rgb(0,0,80)', font_color='rgb(255,255,255)', plot_bgcolor='rgb(0,0,80)',
                          title=name + ' per year in the ' + title_cent + ' century')
    else:
        fig.update_traces(mode='markers+lines')
        fig.update_layout(paper_bgcolor='rgb(0,0,80)', font_color='rgb(255,255,255)', plot_bgcolor='rgb(0,0,80)',
                          title=name + ' per year in the ' + title_cent + ' century', hovermode=hover)
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
    title_cent = ''
    if century[0] == century[1]:
        title_cent += (str(century[0]) + 'th')
    else:
        title_cent += (str(century[0]) + 'th' + '-' + str(century[1]) + 'th')
    fig.update_layout(paper_bgcolor='rgb(0,0,80)', font_color='rgb(255,255,255)', plot_bgcolor='rgb(0,0,80)',
                      title=name + ' in the ' + title_cent + ' century')
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
    fig.update_layout(paper_bgcolor='rgb(0,0,80)', font_color='rgb(255,255,255)', plot_bgcolor='rgb(0,0,80)',
                      title=name + ' per century')
    fig.update_xaxes(type='category')
    return fig


def individual_graph(subject, year):
    selected_df = data.individual_df
    filtered_df = selected_df[selected_df[subject] == 'NL']
    filtered_df = filtered_df[filtered_df['year'] <= year[1]]
    filtered_df = filtered_df[filtered_df['year'] >= year[0]]
    fig = px.scatter(filtered_df, x='day', y='month')
    return fig


# Country heat map
def create_country_map(min_year, max_year):
    merged_df = data.country_df[data.country_df['year'] <= max_year]
    merged_df = merged_df[merged_df['year'] >= min_year]
    merged_df = merged_df[['country', 'count', 'iso_alpha']]
    filtered_df = merged_df.groupby(merged_df['country']).aggregate({'count': 'sum', 'iso_alpha': 'first'})
    filtered_df = filtered_df.reset_index()
    filtered_df = filtered_df.sort_values(by=['count', 'country'], ascending=False)
    fig = px.choropleth(filtered_df, locations='iso_alpha', color='count', hover_name='country',
                                  color_continuous_scale='plasma', labels={'count': 'Number of enrollments'})
    fig.update_layout(paper_bgcolor='rgb(0,0,80)', font_color='rgb(255,255,255)', plot_bgcolor='rgb(0,0,80)',
                                title='Enrollments per country')
    return fig, filtered_df


# subject information table
def create_century_table(df, name):
    table_df = pd.DataFrame(columns=['Statistic', 'Enrollments', 'Century'])
    for cent in df['century'].unique():
        table_df.loc[len(table_df)] = ['Total enrollments', df.loc[df['century'] == cent, 'count'].sum().round(0), cent]
        table_df.loc[len(table_df)] = ['Average enrollments', df.loc[df['century'] == cent, 'count'].mean().round(0), cent]
        table_df.loc[len(table_df)] = [str(name) + ' with the most enrollments',
                                       df.loc[df['century'] == cent].sort_values(by='count', ascending=False).iloc[0][
                                           0].round(0), cent]
        table_df.loc[len(table_df)] = [str(name) + ' with the least enrollments',
                                       df.loc[df['century'] == cent].sort_values(by='count', ascending=False).iloc[0][
                                           0].round(0), cent]
    return table_df


def create_subject_table(df, name, subject, chosen):
    return 0

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
