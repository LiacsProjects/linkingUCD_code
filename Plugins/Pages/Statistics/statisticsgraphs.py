#
# Imports
#
import plotly.express as px
import pandas as pd
from Plugins.helpers import get_variables, merge_years

#
# Statistics information graph
#
def create_statistics_graph(subject):

    selected_df, subjectx, name = get_variables(subject)
    merged_df = merge_years(selected_df, subjectx)

    if subjectx == 'year' or subjectx == 'age':
        merged_df = merged_df.sort_values(by=[subjectx, 'century'], ascending=True)

    fig = px.bar(
        merged_df,
        x='century', y='count',
        color=subjectx,
        color_continuous_scale='blues',
        hover_name=subjectx,
        labels={'century': 'Century', 'count': 'Number of appointments'},)

    fig.update_layout(
        paper_bgcolor='rgba(223,223,218,0.7)',
        font_color='black',
        plot_bgcolor='rgba(223,223,218,0.7)',
        title=name + ' per century',
        modebar_orientation='h',)

    fig.update_xaxes(
        type='category')

    return fig

#
# Statistics of nr of appointments per century table
#
def create_century_table(df, name):

    table_df = pd.DataFrame(columns=['Statistics', 'Appointments'])

    for cent in df['century'].unique():
        table_df.loc[len(table_df)] = \
            ['Century        ', cent * 100]

        table_df.loc[len(table_df)] = \
            ['Sum            ', round(df.loc[df['century'] == cent, 'count'].sum(), 0)]

        table_df.loc[len(table_df)] = \
            ['Average        ', round(df.loc[df['century'] == cent, 'count'].mean(), 0)]

        table_df.loc[len(table_df)] = \
            ['Maximum        ', round(df.loc[df['century'] == cent, 'count'].max(), 0)] #.sort_values(by='count', ascending=False).iloc[0][0]]

        table_df.loc[len(table_df)] = \
            ['Minimum        ', round(df.loc[df['century'] == cent, 'count'].min(), 0)] #sort_values(by='count', ascending=True).iloc[0][0]]

        table_df.loc[len(table_df)] = ['', '']

    return table_df
