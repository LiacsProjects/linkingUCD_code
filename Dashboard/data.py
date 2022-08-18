import pandas as pd

# Professor data handling
#######################################################################################################################
profs_df = pd.read_excel('excelfiles/Hoogleraren.xlsx')
gender_df = pd.read_excel()
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
