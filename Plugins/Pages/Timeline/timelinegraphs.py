#
# Imports
#
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import configparser
import os

from Plugins.Data import exceldata as data

#
# Configure
#
#config = configparser.ConfigParser()
#config.read(os.environ['DASHBOARD_BASEPATH'] + 'assets/config.ini')
#mapbox_token = config['mapbox']['token']

#
# Create graphs
#
def get_variables(subject):
    if subject == 'Gender':
        selected_df = data.gender_df
        subjectx = 'gender'
        name = 'Gender'
    elif subject == 'Title':
        selected_df = data.title_df
        subjectx = 'title'
        name = 'Title'
    elif subject == 'Birth':
        selected_df = data.birth_df
        subjectx = 'birth'
        name = 'Birth'
    elif subject == 'Birth place':
        selected_df = data.birthplace_df
        subjectx = 'birth place'
        name = 'Birth place'
    elif subject == 'Birth country':
        selected_df = data.birthcountry_df
        subjectx = 'country'
        name = 'Birth country'
    elif subject == 'Death':
        selected_df = data.death_df
        subjectx = 'death'
        name = 'Death'
    elif subject == 'Death place':
        selected_df = data.deathplace_df
        subjectx = 'death place'
        name = 'Death place'
    elif subject == 'Death country':
        selected_df = data.deathcountry_df
        subjectx = 'country'
        name = 'Death country'
    elif subject == 'Promotion':
        selected_df = data.promotion_df
        subjectx = 'promotion'
        name = 'Promotion'
    elif subject == 'Promotion type':
        selected_df = data.promotiontype_df
        subjectx = 'promotion type'
        name = 'Promotion type'
    elif subject == 'Promotion place':
        selected_df = data.promotion_place_df
        subjectx = 'promotion place'
        name = 'Promotion place'
    elif subject == 'Appointment':
        selected_df = data.appointment_df
        subjectx = 'appointment'
        name = 'Appointment year'
    elif subject == 'Job':
        selected_df = data.professor_job_df
        subjectx = 'job'
        name = 'Job'
    elif subject == 'Subject area':
        selected_df = data.subject_df
        subjectx = 'subject area'
        name = 'Subject area'
    elif subject == 'Faculty':
        selected_df = data.faculty_df
        subjectx = 'faculty'
        name = 'Faculty'
    elif subject == 'End of employment':
        selected_df = data.end_df
        subjectx = 'end of employment'
        name = 'End of employment'
    else:
        # default setting
        selected_df = data.appointment_df
        subjectx = 'appointment'
        name = 'Appointment year'
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

#
# Yearly graph
#
def create_year_cent_figure(subject, century, year, mode):
    selected_df, subjectx, name = get_variables(subject)
    filtered_df = selected_df[selected_df['century'] <= century[1]]
    filtered_df = filtered_df[filtered_df['century'] >= century[0]]
    filtered_df = filtered_df[filtered_df['year'] <= year[1]]
    filtered_df = filtered_df[filtered_df['year'] >= year[0]]
    if filtered_df.empty:
        fig = px.bar()
        fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black',
                          plot_bgcolor='rgba(223,223,218,0.7)',
                          title="No data in this selection",
                          modebar_orientation='v',)
        return fig
    if filtered_df.iloc[0][subjectx] == filtered_df.iloc[0]['year']:
        bar_color = None
    else:
        bar_color = subjectx
    if mode == 'Line graph':
        fig = px.line(filtered_df, x='year', y='count', color=bar_color,
                      markers=True,
                      labels={subjectx: name, 'count': 'Number of appointments', 'year': 'Year',
                              'century': 'Century'},
                      hover_name=subjectx, hover_data=['year', 'century'])
    elif mode == 'Scatter graph':
        fig = px.scatter(filtered_df, x='year', y=subjectx,
                         size='count',
                         color=bar_color,
                         # color_continuous_scale='blues',
                         log_x=True, labels={subjectx: name, 'count': 'Number of appointments', 'year': 'Year',
                                             'century': 'Century'},
                         hover_name=subjectx, hover_data=['year', 'century'])
    elif mode == 'Bar graph':
        fig = px.bar(filtered_df, x='year', y='count',
                     color=bar_color,
                     # color_continuous_scale='blues',
                     labels={subjectx: name, 'count': 'Number of appointments', 'year': 'Year',
                             'century': 'Century'},
                     hover_name=subjectx, hover_data=['year', 'century'])
    else:
        fig = px.bar()

    if subjectx == 'year':
        title_cent = name + ' per year in the '
    else:
        if name == 'Appointment year':
            title_cent = 'Number of appointments per ' + name + ' in the '
        else:
            title_cent = 'Number of appointments per ' + name + ' per year in the '
    if century[0] == century[1]:
        title_cent += (str(century[0]) + 'th century ')
    else:
        title_cent += (str(century[0]) + 'th' + '-' + str(century[1]) + 'th century')
    if mode == 'Bar graph':
        fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black',
                          plot_bgcolor='rgba(223,223,218,0.7)',
                          title=title_cent,
                          modebar_orientation='v',)
    else:
        # fig.update_traces(mode='lines+markers')
        fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black',
                          plot_bgcolor='rgba(223,223,218,0.7)',
                          title=title_cent,
                          modebar_orientation='v')
    # fig.update_xaxes(type='date')
    return fig

#
# Century graph
#
def create_cent_figure(subject, century):
    selected_df, subjectx, name = get_variables(subject)
    merged_df = merge_years(selected_df, subjectx)
    filtered_df = merged_df[merged_df['century'] <= century[1]]
    filtered_df = filtered_df[filtered_df['century'] >= century[0]]
    if filtered_df.empty:
        fig = px.bar()
        fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black',
                          plot_bgcolor='rgba(223,223,218,0.7)',
                          title="No data in this selection",
                          modebar_orientation='v',)
        return fig
    if subjectx == 'year':
        filtered_df = filtered_df.sort_values(by=[subjectx, 'century'], ascending=True)
    else:
        filtered_df = filtered_df.sort_values(by=['count', 'century'], ascending=False)
    fig = px.bar(filtered_df, x=subjectx, hover_name=subjectx,
                 y='count', hover_data=['century'],
                 labels={subjectx: name, 'count': 'Number of appointments', 'year': 'Year', 'century': 'Century'})
    if subjectx == 'year':
        title_cent = name + ' in the '
    elif subjectx == 'appointment':
        title_cent = 'Number of appointments per ' + name + ' in the '
    else:
        title_cent = 'Number of appointments per ' + name + ' in the '
    if century[0] == century[1]:
        title_cent += (str(century[0]) + 'th century')
    else:
        title_cent += (str(century[0]) + 'th' + '-' + str(century[1]) + 'th century')
    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      title=title_cent,modebar_orientation='v',)
    fig.update_xaxes(type='category')
    return fig
