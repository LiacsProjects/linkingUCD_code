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

def select_non_range(filtered_df, selected_field, column_name):
    temp_df = pd.DataFrame()
    for field in selected_field:  # append all selected
        temp_df = pd.concat([temp_df, filtered_df.loc[filtered_df[column_name] == field]], axis=0)
    # if include_missing == 'Yes':  # append rows where field is empty
    #     temp_df = pd.concat([temp_df, filtered_df.loc[filtered_df['Gender'].isna()]], axis=0)
    filtered_df = temp_df.copy()
    return filtered_df

def select_range(filtered_df, range_min, range_max, column_name, include_missing):
    # Get NaN entries
    temp_missing_df = filtered_df.loc[filtered_df[column_name].isna()]
    # Ranges automatically excludes None values
    filtered_df = filtered_df.loc[filtered_df[column_name] <= int(range_max)]
    filtered_df = filtered_df[filtered_df[column_name] >= int(range_min)]
    if include_missing == 'Yes':  # Reappend temp_missing_df as it was excluded by the ranges
        filtered_df = pd.concat([filtered_df, temp_missing_df], axis=0)
    return filtered_df

