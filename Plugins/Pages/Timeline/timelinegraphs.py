#
# Imports
#
import plotly.express as px

from Plugins.helpers import get_variables, merge_years

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
        title_cent = name + ' in the '
    else:
        if name == 'Appointment year':
            title_cent = 'Appointments per ' + name + ' in the '
        else:
            title_cent = 'Appointments per ' + name + ' per year in the '

    if century[0] == century[1]:
        title_cent += (str(century[0]) + 'th century')
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
# Descending graph
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
        title_cent = 'Descending appointments per ' + name + ' per year in the '
    else:
        title_cent = 'Descending appointments per ' + name + ' in the '

    if century[0] == century[1]:
        title_cent += (str(century[0]) + 'th century')
    else:
        title_cent += (str(century[0]) + 'th' + '-' + str(century[1]) + 'th century')

    fig.update_layout(paper_bgcolor='rgba(223,223,218,0.7)', font_color='black', plot_bgcolor='rgba(223,223,218,0.7)',
                      title=title_cent, modebar_orientation='v',)
    fig.update_xaxes(type='category')

    return fig
