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
from Plugins.helpers import get_variables, merge_years

#
# Statistics information graph
#
def create_subject_info_graph(subject):
    selected_df, subjectx, name = get_variables(subject)
    merged_df = merge_years(selected_df, subjectx)

    if subjectx == 'year' or subjectx == 'age':
        merged_df = merged_df.sort_values(by=[subjectx, 'century'], ascending=True)

    fig = px.bar(merged_df, x='century', y='count', color=subjectx, color_continuous_scale='blues',
                 hover_name=subjectx, labels={'century': 'Century', 'count': 'Number of appointments'},)

    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      title=name + ' per century', modebar_orientation='h',)

    fig.update_xaxes(type='category')
    return fig

#
# Statistics information table
#
def create_century_table(df, name):
    table_df = pd.DataFrame(columns=['Statistic', 'Appointments'])

    for cent in df['century'].unique():
        table_df.loc[len(table_df)] = ['Century', cent]
        table_df.loc[len(table_df)] = ['Total appointments', round(df.loc[df['century'] == cent, 'count'].sum(), 0)]
        table_df.loc[len(table_df)] = ['Average appointments', round(df.loc[df['century'] == cent, 'count'].mean(), 0)]
        table_df.loc[len(table_df)] = ['Most appointments',
                                       df.loc[df['century'] == cent].sort_values(by='count', ascending=False).iloc[0][0]]
        table_df.loc[len(table_df)] = ['Least appointments',
                                       df.loc[df['century'] == cent].sort_values(by='count', ascending=True).iloc[0][0]]
    return table_df
