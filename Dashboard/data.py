import pandas as pd
from pathlib import Path
import os

base_path = Path(os.environ['DASHBOARD_BASEPATH'])

# Professor data handling
#######################################################################################################################
all_dates_df = pd.read_excel(base_path / 'excelfiles/professors_all_dates.xlsx', engine='openpyxl')
dates_df = pd.read_excel(base_path / 'excelfiles/professors_dates.xlsx', engine='openpyxl')

gender_df = pd.read_excel(base_path / 'excelfiles_R/professors_gender.xlsx', engine='openpyxl')
title_df = pd.read_excel(base_path / 'excelfiles_R/professors_title.xlsx', engine='openpyxl')
birth_df = pd.read_excel(base_path / 'excelfiles_R/professors_birth.xlsx', engine='openpyxl')
birthplace_df = pd.read_excel(base_path / 'excelfiles_R/professors_birth_place.xlsx', engine='openpyxl')
birthcountry_df = pd.read_excel(base_path / 'excelfiles_R/professors_birth_country.xlsx', engine='openpyxl')
death_df = pd.read_excel(base_path / 'excelfiles_R/professors_death.xlsx', engine='openpyxl')
deathplace_df = pd.read_excel(base_path / 'excelfiles_R/professors_death_place.xlsx', engine='openpyxl')
deathcountry_df = pd.read_excel(base_path / 'excelfiles_R/professors_death_country.xlsx', engine='openpyxl')
promotion_df = pd.read_excel(base_path / 'excelfiles_R/professors_promotion.xlsx', engine='openpyxl')
promotiontype_df = pd.read_excel(base_path / 'excelfiles_R/professors_promotion_type.xlsx', engine='openpyxl')
promotion_place_df = pd.read_excel(base_path / 'excelfiles_R/professors_promotion_place.xlsx', engine='openpyxl')
appointment_df = pd.read_excel(base_path / 'excelfiles_R/professors_appointment.xlsx', engine='openpyxl')
professor_job_df = pd.read_excel(base_path / 'excelfiles_R/professors_job.xlsx', engine='openpyxl')
subject_df = pd.read_excel(base_path / 'excelfiles_R/professors_subject.xlsx', engine='openpyxl')
faculty_df = pd.read_excel(base_path / 'excelfiles_R/professors_faculty.xlsx', engine='openpyxl')
end_df = pd.read_excel(base_path / 'excelfiles_R/professors_end.xlsx', engine='openpyxl')
individual_profs_df = pd.read_excel(base_path / 'excelfiles_R/professors_individual.xlsx', engine='openpyxl')

#######################################################################################################################

# Student data handling
#######################################################################################################################
century_df = pd.read_excel(base_path / 'excelfiles/students_century.xlsx', engine='openpyxl')
year_df = pd.read_excel(base_path / 'excelfiles/students_years.xlsx', engine='openpyxl')
country_df = pd.read_excel(base_path / 'excelfiles/students_country.xlsx', engine='openpyxl')
city_df = pd.read_excel(base_path / 'excelfiles/students_city.xlsx', engine='openpyxl')
region_df = pd.read_excel(base_path / 'excelfiles/students_region.xlsx', engine='openpyxl')
age_df = pd.read_excel(base_path / 'excelfiles/students_age.xlsx', engine='openpyxl')
fac_df = pd.read_excel(base_path / 'excelfiles/students_faculty.xlsx', engine='openpyxl')
extra_df = pd.read_excel(base_path / 'excelfiles/students_extra.xlsx', engine='openpyxl')
gratis_df = pd.read_excel(base_path / 'excelfiles/students_gratis.xlsx', engine='openpyxl')
status_df = pd.read_excel(base_path / 'excelfiles/students_status.xlsx', engine='openpyxl')
job_df = pd.read_excel(base_path / 'excelfiles/students_job.xlsx', engine='openpyxl')
rel_df = pd.read_excel(base_path / 'excelfiles/students_rel.xlsx', engine='openpyxl')
previous_df = pd.read_excel(base_path / 'excelfiles/students_previous.xlsx', engine='openpyxl')
individual_student_df = pd.read_excel(base_path / 'excelfiles/students_individual.xlsx', engine='openpyxl')

#######################################################################################################################
# Rectores Magnifici data handling
#######################################################################################################################
recmag_df = pd.read_excel(base_path / 'excelfiles/recmag.xlsx', engine='openpyxl')

rector_term_start = recmag_df['Period_start']

rector_term_end = recmag_df['Period_end']

rector_century = recmag_df['century']

rector_years = pd.DataFrame(recmag_df['Period_start'].unique())
rector_years = rector_years.rename(columns={0: 'year'})
rector_years['century'] = rector_years['year'].astype(str).str[:2].astype(int) + 1

rector_terms = recmag_df['Period_start'].value_counts()

rector_names = recmag_df[['Name', 'Period_start', 'century']]

rector_pictures = recmag_df['Picture_saved']

rector_details = recmag_df['Term/Details']

rector_per_year = recmag_df['Period_start'].value_counts().reset_index()
rector_per_year = rector_per_year.sort_values(by=['Period_start'], axis=0, ascending=True)
#rector_per_year = recmag_df['Period_start'].value_counts().reset_index().sort_values(by=['index'], ascending=True)
rector_per_year = rector_per_year.rename(columns={'Period_start': 'year'})
rector_per_year['century'] = rector_per_year['year'].astype(str).str[:2].astype(int) + 1
#######################################################################################################################
