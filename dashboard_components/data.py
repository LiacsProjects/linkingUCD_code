import pandas as pd
from pathlib import Path
import os
import time
from Adapters import database

# 'C:/Users/micha/Documents/Leiden/Univercity/Database_Connected_Dashboard/Dashboard/'
bp = 'C:/Users/micha/Documents/Leiden/Univercity/Database_Connected_Dashboard/Liam/excelfiles/'
base_path = Path(os.environ['DASHBOARD_BASEPATH'])

conn = database.Connection()
# Professor data handling
start = time.time()
print("Start professor")
#######################################################################################################################
yearList = range(1520, 2020)
centuryList = [i // 100 if i % 100 == 0 else i // 100 + 1 for i in range(1520, 2020)]
# centuryList = [i // 100 + 1 for i in range(1520, 2020)]
all_dates_df = pd.DataFrame({'year': yearList, 'century': centuryList})

# dates_df redundant? Commented for now
# dates_df = pd.read_excel(base_path / 'excelfiles/professors_dates.xlsx', engine='openpyxl')

gender_df = conn.QueryBuilderPublic(['Gender'], ['profession'], "gender", "professor", [])
title_df = pd.read_excel(base_path / 'excelfiles/professors_title.xlsx', engine='openpyxl')
birth_df = conn.QueryBuilderPublic(['StartDate'], ['location'], "birth", "professor", ["TypeOfLocation = 1"])
birthplace_df = conn.QueryBuilderPublic(['City'], ['location'], "birth place", "professor", ["TypeOfLocation = 1"])
birthcountry_df = conn.QueryBuilderPublic(['Country'], ['location'], "country", "professor", ["TypeOfLocation = 1"])  # TODO add coords
death_df = conn.QueryBuilderPublic(['StartDate'], ['location'], "death", "professor", ["TypeOfLocation = 2"])
deathplace_df = conn.QueryBuilderPublic(['City'], ['location'], "death place", "professor", ["TypeOfLocation = 2"])
deathcountry_df = conn.QueryBuilderPublic(['Country'], ['location'], "country", "professor", ["TypeOfLocation = 2"])  # TODO add coords
promotion_df = pd.read_excel(base_path / 'excelfiles/professors_promotion.xlsx', engine='openpyxl')
promotiontype_df = pd.read_excel(base_path / 'excelfiles/professors_promotion_type.xlsx', engine='openpyxl')
promotion_place_df = pd.read_excel(base_path / 'excelfiles/professors_promotion_place.xlsx', engine='openpyxl')
appointment_df = conn.QueryBuilderPublic(['StartDate'], ['profession'], "appointment", "professor", ["TypeOfProfession = 2"])
professor_job_df = conn.QueryBuilderPublic(['PositionType'], ['profession', 'type_of_position'], "job", "professor", [])
subject_df = conn.QueryBuilderPublic(['ExpertiseType'], ['profession', 'type_of_expertise'], "subject area", "professor", [])
faculty_df = conn.QueryBuilderPublic(['FacultyType'], ['profession', 'type_of_faculty'], "faculty", "professor", [])
end_df = conn.QueryBuilderPublic(['EndDate'], ['profession'], "end of employment", "professor", ["TypeOfProfession = 2"])
individual_profs_df = pd.read_excel(base_path / 'excelfiles/professors_individual.xlsx', engine='openpyxl')
print(f"Professors finished in {time.time() - start} seconds")
#######################################################################################################################

# Student data handling
#######################################################################################################################
start = time.time()  # Takes roughly 14 seconds with Excel
print("Start student")
century_df = pd.read_excel(base_path / 'excelfiles/students_century.xlsx', engine='openpyxl')  # Other format
year_df = pd.read_excel(base_path / 'excelfiles/students_years.xlsx', engine='openpyxl')  # Other format
country_df = pd.read_excel(base_path / 'excelfiles/students_country.xlsx', engine='openpyxl')
# country_df = conn.QueryBuilderPublic(['Country'], ['location'], "country", "student", ["TypeOfLocation = 1"])  # TODO add coords

# city_df = pd.read_excel(base_path / 'excelfiles/students_city.xlsx', engine='openpyxl')
city_df = conn.QueryBuilderPublic(['City'], ['location'], "city", "student", ["TypeOfLocation = 1"])
# region_df = pd.read_excel(base_path / 'excelfiles/students_region.xlsx', engine='openpyxl')
region_df = conn.QueryBuilderPublic(['Region'], ['location'], "region", "student", ["TypeOfLocation = 1"])

age_df = pd.read_excel(base_path / 'excelfiles/students_age.xlsx', engine='openpyxl')
fac_df = pd.read_excel(base_path / 'excelfiles/students_faculty.xlsx', engine='openpyxl')
extra_df = pd.read_excel(base_path / 'excelfiles/students_extra.xlsx', engine='openpyxl')
gratis_df = pd.read_excel(base_path / 'excelfiles/students_gratis.xlsx', engine='openpyxl')
status_df = pd.read_excel(base_path / 'excelfiles/students_status.xlsx', engine='openpyxl')
job_df = pd.read_excel(base_path / 'excelfiles/students_job.xlsx', engine='openpyxl')
rel_df = pd.read_excel(base_path / 'excelfiles/students_rel.xlsx', engine='openpyxl')
previous_df = pd.read_excel(base_path / 'excelfiles/students_previous.xlsx', engine='openpyxl')
individual_student_df = pd.read_excel(base_path / 'excelfiles/students_individual.xlsx', engine='openpyxl')

print(f"Students finished in {time.time() - start} seconds")

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

# Attention!!! Uncomment the 3 lines below if it does not produce any errors
# rector_per_year = recmag_df['Period_start'].value_counts().reset_index().sort_values(by=['index'], ascending=True)
# rector_per_year = rector_per_year.rename(columns={'index': 'year', 'Period_start': 'count'})
# rector_per_year['century'] = rector_per_year['year'].astype(str).str[:2].astype(int) + 1
#######################################################################################################################
del conn

# import pandas as pd
# from pathlib import Path
# import os
# import time
#
#
# bp = 'C:/Users/micha/Documents/Leiden/Univercity/Database_Connected_Dashboard/Liam/excelfiles/'
# base_path = Path(os.environ['DASHBOARD_BASEPATH'])
#
# # Professor data handling
# start = time.time()
# #######################################################################################################################
# all_dates_df = pd.read_excel(base_path / 'excelfiles/professors_all_dates.xlsx', engine='openpyxl')
# dates_df = pd.read_excel(base_path / 'excelfiles/professors_dates.xlsx', engine='openpyxl')
#
# gender_df = pd.read_excel(base_path / 'excelfiles/professors_gender.xlsx', engine='openpyxl')
# title_df = pd.read_excel(base_path / 'excelfiles/professors_title.xlsx', engine='openpyxl')
# birth_df = pd.read_excel(base_path / 'excelfiles/professors_birth.xlsx', engine='openpyxl')
# birthplace_df = pd.read_excel(base_path / 'excelfiles/professors_birth_place.xlsx', engine='openpyxl')
# birthcountry_df = pd.read_excel(base_path / 'excelfiles/professors_birth_country.xlsx', engine='openpyxl')
# death_df = pd.read_excel(base_path / 'excelfiles/professors_death.xlsx', engine='openpyxl')
# deathplace_df = pd.read_excel(base_path / 'excelfiles/professors_death_place.xlsx', engine='openpyxl')
# deathcountry_df = pd.read_excel(base_path / 'excelfiles/professors_death_country.xlsx', engine='openpyxl')
# promotion_df = pd.read_excel(base_path / 'excelfiles/professors_promotion.xlsx', engine='openpyxl')
# promotiontype_df = pd.read_excel(base_path / 'excelfiles/professors_promotion_type.xlsx', engine='openpyxl')
# promotion_place_df = pd.read_excel(base_path / 'excelfiles/professors_promotion_place.xlsx', engine='openpyxl')
# appointment_df = pd.read_excel(base_path / 'excelfiles/professors_appointment.xlsx', engine='openpyxl')
# professor_job_df = pd.read_excel(base_path / 'excelfiles/professors_job.xlsx', engine='openpyxl')
# subject_df = pd.read_excel(base_path / 'excelfiles/professors_subject.xlsx', engine='openpyxl')
# faculty_df = pd.read_excel(base_path / 'excelfiles/professors_faculty.xlsx', engine='openpyxl')
# end_df = pd.read_excel(base_path / 'excelfiles/professors_end.xlsx', engine='openpyxl')
# individual_profs_df = pd.read_excel(base_path / 'excelfiles/professors_individual.xlsx', engine='openpyxl')
# print(f"Program finished successfully in {time.time() - start} seconds")
#
# #######################################################################################################################
#
# # Student data handling
# #######################################################################################################################
# century_df = pd.read_excel(base_path / 'excelfiles/students_century.xlsx', engine='openpyxl')
# year_df = pd.read_excel(base_path / 'excelfiles/students_years.xlsx', engine='openpyxl')
# country_df = pd.read_excel(base_path / 'excelfiles/students_country.xlsx', engine='openpyxl')
# city_df = pd.read_excel(base_path / 'excelfiles/students_city.xlsx', engine='openpyxl')
# region_df = pd.read_excel(base_path / 'excelfiles/students_region.xlsx', engine='openpyxl')
# age_df = pd.read_excel(base_path / 'excelfiles/students_age.xlsx', engine='openpyxl')
# fac_df = pd.read_excel(base_path / 'excelfiles/students_faculty.xlsx', engine='openpyxl')
# extra_df = pd.read_excel(base_path / 'excelfiles/students_extra.xlsx', engine='openpyxl')
# gratis_df = pd.read_excel(base_path / 'excelfiles/students_gratis.xlsx', engine='openpyxl')
# status_df = pd.read_excel(base_path / 'excelfiles/students_status.xlsx', engine='openpyxl')
# job_df = pd.read_excel(base_path / 'excelfiles/students_job.xlsx', engine='openpyxl')
# rel_df = pd.read_excel(base_path / 'excelfiles/students_rel.xlsx', engine='openpyxl')
# previous_df = pd.read_excel(base_path / 'excelfiles/students_previous.xlsx', engine='openpyxl')
# individual_student_df = pd.read_excel(base_path / 'excelfiles/students_individual.xlsx', engine='openpyxl')
#
# #######################################################################################################################
# # Rectores Magnifici data handling
# #######################################################################################################################
# recmag_df = pd.read_excel(base_path / 'excelfiles/recmag.xlsx', engine='openpyxl')
#
# rector_term_start = recmag_df['Period_start']
#
# rector_term_end = recmag_df['Period_end']
#
# rector_century = recmag_df['century']
#
# rector_years = pd.DataFrame(recmag_df['Period_start'].unique())
# rector_years = rector_years.rename(columns={0: 'year'})
# rector_years['century'] = rector_years['year'].astype(str).str[:2].astype(int) + 1
#
# rector_terms = recmag_df['Period_start'].value_counts()
#
# rector_names = recmag_df[['Name', 'Period_start', 'century']]
#
# rector_pictures = recmag_df['Picture_saved']
#
# rector_details = recmag_df['Term/Details']
#
# # df1 = pd.DataFrame(data=recmag_df['Period_start'].values, columns=["index", "Period_start"])
# # rector_per_year = pd.DataFrame({'email':recmag_df['Period_start'].index, 'list':recmag_df['Period_start'].values})
# # recmag_df['Period_start'].index.name = 'index'
# # rector_per_year = recmag_df['Period_start'].value_counts().reset_index().sort_values(by=['index'], axis='index', ascending=True)
# # rector_per_year = recmag_df['Period_start'].value_counts().reset_index()
# # rector_per_year = rector_per_year.rename(columns={'index': 'year', 'Period_start': 'count'})
#
# # rector_per_year = rector_per_year.rename(columns={'Period_start': 'count'})
# # rector_per_year['century'] = rector_per_year['year'].astype(str).str[:2].astype(int) + 1
#######################################################################################################################
