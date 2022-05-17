import pandas as pd

profs_df = pd.read_excel('Hoogleraren.xlsx')
students_df = pd.read_excel('Alle inschrijvingen 1575-1812.xlsx')
recmag_df = pd.read_csv('recmag_v1.csv')

# Professor data handling
#######################################################################################################################
profs_df[['bd', 'bm', 'by']] = profs_df['Geboortedatum'].str.split('-', expand=True)
profs_df[['dd', 'dm', 'dy']] = profs_df['Sterfdatum'].str.split('-', expand=True)
profs_df[['prod', 'prom', 'proy']] = profs_df['Datum'].str.split('-', expand=True)
profs_df[['aan1d', 'aan1m', 'aan1y']] = profs_df['Datum aanstelling I'].str.split('-', expand=True)
profs_df[['amb1d', 'amb1m', 'amb1y']] = profs_df['Ambtsaanvaarding I'].str.split('-', expand=True)
profs_df[['or1d', 'or1m', 'or1y']] = profs_df['Datum oratie I'].str.split('-', expand=True)
profs_df[['ed1d', 'ed1m', 'ed1y']] = profs_df['Einde dienstverband I'].str.split('-', expand=True)
profs_df[['aan2d', 'aan2m', 'aan2y']] = profs_df['Datum aanstelling II'].str.split('-', expand=True)
profs_df[['amb2d', 'amb2m', 'amb2y']] = profs_df['Ambtsaanvaarding II'].str.split('-', expand=True)
profs_df[['or2d', 'or2m', 'or2y']] = profs_df['Datum oratie II'].str.split('-', expand=True)
profs_df[['ed2d', 'ed2m', 'ed2y']] = profs_df['Einde dienstverband II'].str.split('-', expand=True)
profs_df[['aan3d', 'aan3m', 'aan3y']] = profs_df['Datum aanstelling III'].str.split('-', expand=True)
profs_df[['amb3d', 'amb3m', 'amb3y']] = profs_df['Ambtsaanvaarding III'].str.split('-', expand=True)
profs_df[['or3d', 'or3m', 'or3y']] = profs_df['Datum oratie III'].str.split('-', expand=True)
profs_df[['ed3d', 'ed3m', 'ed3y']] = profs_df['Einde dienstverband III'].str.split('-', expand=True)
profs_df[['aan4d', 'aan4m', 'aan4y']] = profs_df['Datum aanstelling IV'].str.split('-', expand=True)
profs_df[['amb4d', 'amb4m', 'amb4y']] = profs_df['Ambtsaanvaarding IV'].str.split('-', expand=True)
profs_df[['or4d', 'or4m', 'or4y']] = profs_df['Datum oratie IV'].str.split('-', expand=True)
profs_df[['ed4d', 'ed4m', 'ed4y']] = profs_df['Einde dienstverband IV'].str.split('-', expand=True)

for idx, row in profs_df.iterrows():
    value = len(str(row['bd']))
    if value > 2:
        profs_df.loc[idx, 'by'] = row['bd']
        profs_df.loc[idx, 'bd'] = None
    value = len(str(row['dd']))
    if value > 2:
        profs_df.loc[idx, 'dy'] = row['dd']
        profs_df.loc[idx, 'dd'] = None
    value = len(str(row['prod']))
    if value > 2:
        profs_df.loc[idx, 'proy'] = row['prod']
        profs_df.loc[idx, 'prod'] = None
    value = len(str(row['aan1d']))
    if value > 2:
        profs_df.loc[idx, 'aan1y'] = row['aan1d']
        profs_df.loc[idx, 'aan1d'] = None
    value = len(str(row['amb1d']))
    if value > 2:
        profs_df.loc[idx, 'amb1y'] = row['amb1d']
        profs_df.loc[idx, 'amb1d'] = None
    value = len(str(row['or1d']))
    if value > 2:
        profs_df.loc[idx, 'or1y'] = row['or1d']
        profs_df.loc[idx, 'or1d'] = None
    value = len(str(row['ed1d']))
    if value > 2:
        profs_df.loc[idx, 'ed1y'] = row['ed1d']
        profs_df.loc[idx, 'ed1d'] = None
    value = len(str(row['aan2d']))
    if value > 2:
        profs_df.loc[idx, 'aan2y'] = row['aan2d']
        profs_df.loc[idx, 'aan2d'] = None
    value = len(str(row['amb2d']))
    if value > 2:
        profs_df.loc[idx, 'amb2y'] = row['amb2d']
        profs_df.loc[idx, 'amb2d'] = None
    value = len(str(row['or2d']))
    if value > 2:
        profs_df.loc[idx, 'or2y'] = row['or2d']
        profs_df.loc[idx, 'or2d'] = None
    value = len(str(row['ed2d']))
    if value > 2:
        profs_df.loc[idx, 'ed2y'] = row['ed2d']
        profs_df.loc[idx, 'ed2d'] = None
    value = len(str(row['aan3d']))
    if value > 2:
        profs_df.loc[idx, 'aan3y'] = row['aan3d']
        profs_df.loc[idx, 'aan3d'] = None
    value = len(str(row['amb3d']))
    if value > 2:
        profs_df.loc[idx, 'amb3y'] = row['amb3d']
        profs_df.loc[idx, 'amb3d'] = None
    value = len(str(row['or3d']))
    if value > 2:
        profs_df.loc[idx, 'or3y'] = row['or3d']
        profs_df.loc[idx, 'or3d'] = None
    value = len(str(row['ed3d']))
    if value > 2:
        profs_df.loc[idx, 'ed3y'] = row['ed3d']
        profs_df.loc[idx, 'ed3d'] = None
    value = len(str(row['aan4d']))
    if value > 2:
        profs_df.loc[idx, 'aan4y'] = row['aan4d']
        profs_df.loc[idx, 'aan4d'] = None
    value = len(str(row['amb4d']))
    if value > 2:
        profs_df.loc[idx, 'amb4y'] = row['amb4d']
        profs_df.loc[idx, 'amb4d'] = None
    value = len(str(row['or4d']))
    if value > 2:
        profs_df.loc[idx, 'or4y'] = row['or4d']
        profs_df.loc[idx, 'or4d'] = None
    value = len(str(row['ed4d']))
    if value > 2:
        profs_df.loc[idx, 'ed4y'] = row['ed4d']
        profs_df.loc[idx, 'ed4d'] = None

# Data (totaal)


# Geboortejaar

# Sterftejaar

# Geboorte/sterfte (totaal)

# Geboorteplaats

# Geboorteland

# Sterfteplaats

# Sterfteland

# Promotie (totaal)

# Promotietype

# Promotieinstelling

# Promotiedatum

# Promotieproefschrift

# Dienstverband (totaal)

# Aanstellingpositie

# Aanstellingsdatum

# Ambtsaanvaardingsdatum

# Vakgebied

# Oratie

# Faculteit

# Datum einde dienstverband

# Reden einde dienstverband

# Bijzonderheden
#######################################################################################################################

# Student data handling
#######################################################################################################################
# Split dataframe per year
def split_years(df):
    return [df[df['DATUMJAAR_as']==y]for y in df['DATUMJAAR_as'].unique()]


# Create value counts for given subject
def create_value_counts(df, name, subject):
    total_df = pd.DataFrame()
    for year in df:
        temp_df = pd.DataFrame(year)
        current_year = temp_df['DATUMJAAR_as'].iloc[0]
        current_century = temp_df['EEUW'].iloc[0]
        tempvc_df = temp_df[subject].value_counts()
        tempvc_df = tempvc_df.reset_index()
        tempvc_df['year'] = current_year
        tempvc_df['century'] = current_century
        total_df = pd.concat([total_df, tempvc_df], axis=0)
    if name == 'year' or name == 'century':
        total_df.drop('index', axis=1, inplace=True)
        total_df = total_df.rename(columns={subject: 'count'})
    else:
        total_df = total_df.rename(columns={'index': name, subject: 'count'})
    #if total_df[name].dtypes == 'int64' or total_df[name].dtypes == 'float64':
        #total_df = total_df.sort_values(by =['century', 'year', name])
    total_df.reset_index(inplace=True, drop=True)
    return total_df


# Fix wrong input
find_nl = students_df.loc[students_df['LAND'] == 'nl']
students_df.at[find_nl.index[0], 'LAND'] = 'NL'
# Split dataframe
students2_df = split_years(students_df)

# Century
century_df = create_value_counts(students2_df, 'century', 'EEUW')

# Year
year_df = create_value_counts(students2_df, 'year', 'DATUMJAAR_as')

# Country
country_df = create_value_counts(students2_df, 'country', 'LAND')
country_df = country_df[country_df.country != '-']
country_df = country_df[country_df.country != '?']
country_df.loc[country_df.country == 'NL', 'iso_alpha'] = 'NLD'
country_df.loc[country_df.country == 'Z-NL', 'iso_alpha'] = 'BEL'
country_df.loc[country_df.country == 'Duitsland', 'iso_alpha'] = 'DEU'
country_df.loc[country_df.country == 'Britse eilanden', 'iso_alpha'] = 'GBR'
country_df.loc[country_df.country == 'Frankrijk', 'iso_alpha'] = 'FRA'
country_df.loc[country_df.country == 'Denemarken', 'iso_alpha'] = 'DNK'
country_df.loc[country_df.country == 'Polen', 'iso_alpha'] = 'POL'
country_df.loc[country_df.country == 'Zwitserland', 'iso_alpha'] = 'CHE'
country_df.loc[country_df.country == 'Italie', 'iso_alpha'] = 'ITA'
country_df.loc[country_df.country == 'Zweden', 'iso_alpha'] = 'SWE'
country_df.loc[country_df.country == 'Hongarije', 'iso_alpha'] = 'HUN'
country_df.loc[country_df.country == 'Noorwegen', 'iso_alpha'] = 'NOR'
country_df.loc[country_df.country == 'Rusland', 'iso_alpha'] = 'RUS'
country_df.loc[country_df.country == 'Portugal', 'iso_alpha'] = 'PRT'
country_df.loc[country_df.country == 'Finland', 'iso_alpha'] = 'FIN'
country_df.loc[country_df.country == 'Spanje', 'iso_alpha'] = 'ESP'
country_df.loc[country_df.country == 'Afrika', 'iso_alpha'] = 'MAR'
country_df.loc[country_df.country == 'Ijsland', 'iso_alpha'] = 'ISL'
country_df.loc[country_df.country == 'Arabie', 'iso_alpha'] = 'IRN'
country_df.loc[country_df.country == 'Maltha', 'iso_alpha'] = 'MLT'

# City
city_df = create_value_counts(students2_df, 'city', 'VERT_PLAATS')

# Region
region_df = create_value_counts(students2_df, 'region', 'REGIO2_WERELDDEEL')

# Age
age_df = create_value_counts(students2_df, 'age', 'LEEFTIJD_as')

# Faculty
fac_df = create_value_counts(students2_df, 'faculty', 'VERT_FAC')

# Extra
extra_df = create_value_counts(students2_df, 'extra', 'VERT_AANVULLING')

# Gratis
gratis_df = create_value_counts(students2_df, 'gratis', 'GRATIS_as')

# Status
status_df = create_value_counts(students2_df, 'status', 'STATUS_INGESCHREVENE')
status_df = status_df[status_df.status != 'Edele ?']
status_df = status_df[status_df.status != 'Controleer']
status_df = status_df[status_df.status != 'Edele ? C nog']

# Job
job_df = create_value_counts(students2_df, 'job', 'BEROEP_INGESCHREVENE')

# Religion
rel_df = create_value_counts(students2_df, 'religion', 'RELIGIE_INGESCHREVENE')

# Previous Enrollments
previous_df = create_value_counts(students2_df, 'previous', 'INS_KEER')

#######################################################################################################################

# Rectores Magnifici data handling
#######################################################################################################################


#######################################################################################################################
