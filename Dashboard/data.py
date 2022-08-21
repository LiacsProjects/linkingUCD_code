import pandas as pd

# Professor data handling
#######################################################################################################################
all_dates_df = pd.read_excel('excelfiles/professors_all_dates.xlsx')
dates_df = pd.read_excel('excelfiles/professors_dates.xlsx')
gender_df = pd.read_excel('excelfiles/professors_gender.xlsx')
title_df = pd.read_excel('excelfiles/professors_title.xlsx')
birth_df = pd.read_excel('excelfiles/professors_birth.xlsx')
birthplace_df = pd.read_excel('excelfiles/professors_birth_place.xlsx')
birthcountry_df = pd.read_excel('excelfiles/professors_birth_country.xlsx')
death_df = pd.read_excel('excelfiles/professors_death.xlsx')
deathplace_df = pd.read_excel('excelfiles/professors_death_place.xlsx')
deathcountry_df = pd.read_excel('excelfiles/professors_death_country.xlsx')
promotion_df = pd.read_excel('excelfiles/professors_promotion.xlsx')
promotiontype_df = pd.read_excel('excelfiles/professors_promotion_type.xlsx')
promotion_place_df = pd.read_excel('excelfiles/professors_promotion_place.xlsx')
appointment_df = pd.read_excel('excelfiles/professors_appointment.xlsx')
job_df = pd.read_excel('excelfiles/professors_job.xlsx')
subject_df = pd.read_excel('excelfiles/professors_subject.xlsx')
faculty_df = pd.read_excel('excelfiles/professors_faculty.xlsx')
end_df = pd.read_excel('excelfiles/professors_end.xlsx')
individual_profs_df = pd.read_excel('excelfiles/professors_individual.xlsx')

#######################################################################################################################

# Student data handling
#######################################################################################################################
century_df = pd.read_excel('excelfiles/students_century.xlsx')
year_df = pd.read_excel('excelfiles/students_years.xlsx')
country_df = pd.read_excel('excelfiles/students_country.xlsx')
city_df = pd.read_excel('excelfiles/students_city.xlsx')
region_df = pd.read_excel('excelfiles/students_region.xlsx')
age_df = pd.read_excel('excelfiles/students_age.xlsx')
fac_df = pd.read_excel('excelfiles/students_faculty.xlsx')
extra_df = pd.read_excel('excelfiles/students_extra.xlsx')
gratis_df = pd.read_excel('excelfiles/students_gratis.xlsx')
status_df = pd.read_excel('excelfiles/students_status.xlsx')
job_df = pd.read_excel('excelfiles/students_job.xlsx')
rel_df = pd.read_excel('excelfiles/students_rel.xlsx')
previous_df = pd.read_excel('excelfiles/students_previous.xlsx')
individual_df = pd.read_excel('excelfiles/students_individual.xlsx')

#######################################################################################################################
# Rectores Magnifici data handling
#######################################################################################################################
recmag_df = pd.read_excel('excelfiles/recmag.xlsx')

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

rector_per_year = recmag_df['Period_start'].value_counts().reset_index().sort_values(by=['index'], ascending=True)
rector_per_year = rector_per_year.rename(columns={'index': 'year', 'Period_start': 'count'})
rector_per_year['century'] = rector_per_year['year'].astype(str).str[:2].astype(int) + 1
#######################################################################################################################
