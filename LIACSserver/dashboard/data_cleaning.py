import pandas as pd
import numpy as np


def split_years(df, year_column):
    return [df[df[year_column] == y] for y in df[year_column].unique()]


# Create value counts for given subject
def create_value_counts_professor(df, name, subject, chosen_year, century):
    total_df = pd.DataFrame()
    for year in df:
        temp_df = pd.DataFrame(year)
        current_year = temp_df[chosen_year].iloc[0]
        current_century = temp_df[century].iloc[0]
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
    total_df.reset_index(inplace=True, drop=True)
    return total_df


def create_value_counts_students(df, name, subject):
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
    total_df.reset_index(inplace=True, drop=True)
    return total_df


def add_country_info(df):
    df.loc[df.country == 'Nederland', 'iso_alpha'] = 'NLD'
    df.loc[df.country == 'Nederland', 'lat'] = '52.132633'
    df.loc[df.country == 'Nederland', 'lon'] = '5.291266'
    df.loc[df.country == 'Belgie', 'iso_alpha'] = 'BEL'
    df.loc[df.country == 'Belgie', 'lat'] = '50.503887'
    df.loc[df.country == 'Belgie', 'lon'] = '4.469936'
    df.loc[df.country == 'Duitsland', 'iso_alpha'] = 'DEU'
    df.loc[df.country == 'Duitsland', 'lat'] = '51.165691'
    df.loc[df.country == 'Duitsland', 'lon'] = '10.451526'
    df.loc[df.country == 'Britse eilanden', 'iso_alpha'] = 'GBR'
    df.loc[df.country == 'Britse eilanden', 'lat'] = '55.378051'
    df.loc[df.country == 'Britse eilanden', 'lon'] = '-3.435973'
    df.loc[df.country == 'Frankrijk', 'iso_alpha'] = 'FRA'
    df.loc[df.country == 'Frankrijk', 'lat'] = '46.227638'
    df.loc[df.country == 'Frankrijk', 'lon'] = '2.213749'
    df.loc[df.country == 'Denemarken', 'iso_alpha'] = 'DNK'
    df.loc[df.country == 'Denemarken', 'lat'] = '56.26392'
    df.loc[df.country == 'Denemarken', 'lon'] = '9.501785'
    df.loc[df.country == 'Polen', 'iso_alpha'] = 'POL'
    df.loc[df.country == 'Polen', 'lat'] = '51.919438'
    df.loc[df.country == 'Polen', 'lon'] = '19.145136'
    df.loc[df.country == 'Zwitserland', 'iso_alpha'] = 'CHE'
    df.loc[df.country == 'Zwitserland', 'lat'] = '49.817492'
    df.loc[df.country == 'Zwitserland', 'lon'] = '15.472962'
    df.loc[df.country == 'Italie', 'iso_alpha'] = 'ITA'
    df.loc[df.country == 'Italie', 'lat'] = '41.87194'
    df.loc[df.country == 'Italie', 'lon'] = '12.56738'
    df.loc[df.country == 'Zweden', 'iso_alpha'] = 'SWE'
    df.loc[df.country == 'Zweden', 'lat'] = '60.128161'
    df.loc[df.country == 'Zweden', 'lon'] = '18.643501'
    df.loc[df.country == 'Hongarije', 'iso_alpha'] = 'HUN'
    df.loc[df.country == 'Hongarije', 'lat'] = '47.162494'
    df.loc[df.country == 'Hongarije', 'lon'] = '19.503304'
    df.loc[df.country == 'Noorwegen', 'iso_alpha'] = 'NOR'
    df.loc[df.country == 'Noorwegen', 'lat'] = '60.472024'
    df.loc[df.country == 'Noorwegen', 'lon'] = '8.468946'
    df.loc[df.country == 'Rusland', 'iso_alpha'] = 'RUS'
    df.loc[df.country == 'Rusland', 'lat'] = '61.52401'
    df.loc[df.country == 'Rusland', 'lon'] = '105.318756'
    df.loc[df.country == 'Portugal', 'iso_alpha'] = 'PRT'
    df.loc[df.country == 'Portugal', 'lat'] = '39.399872'
    df.loc[df.country == 'Portugal', 'lon'] = '-8.224454'
    df.loc[df.country == 'Finland', 'iso_alpha'] = 'FIN'
    df.loc[df.country == 'Finland', 'lat'] = '61.92411'
    df.loc[df.country == 'Finland', 'lon'] = '25.748151'
    df.loc[df.country == 'Spanje', 'iso_alpha'] = 'ESP'
    df.loc[df.country == 'Spanje', 'lat'] = '40.463667'
    df.loc[df.country == 'Spanje', 'lon'] = '-3.74922'
    df.loc[df.country == 'Afrika', 'iso_alpha'] = 'MAR'
    df.loc[df.country == 'Afrika', 'lat'] = '31.791702'
    df.loc[df.country == 'Afrika', 'lon'] = '-7.09262'
    df.loc[df.country == 'IJsland', 'iso_alpha'] = 'ISL'
    df.loc[df.country == 'IJsland', 'lat'] = '64.963051'
    df.loc[df.country == 'IJsland', 'lon'] = '-19.020835'
    df.loc[df.country == 'Arabie', 'iso_alpha'] = 'IRN'
    df.loc[df.country == 'Arabie', 'lat'] = '32.427908'
    df.loc[df.country == 'Arabie', 'lon'] = '53.688046'
    df.loc[df.country == 'Maltha', 'iso_alpha'] = 'MLT'
    df.loc[df.country == 'Maltha', 'lat'] = '35.937496'
    df.loc[df.country == 'Maltha', 'lon'] = '14.375416'
    df.loc[df.country == 'Osmaanse rijk', 'iso_alpha'] = 'TUR'
    df.loc[df.country == 'Osmaanse rijk', 'lat'] = '38.963745'
    df.loc[df.country == 'Osmaanse rijk', 'lon'] = '35.243322'
    return df


def clean_professor_data():
    profs_df = pd.read_excel('excelfiles/Hoogleraren.xlsx')
    # Split dates
    profs_df[['birth_day', 'birth_month', 'birth_year']] = profs_df['Geboortedatum'].str.split('-', expand=True)
    profs_df[['death_day', 'death_month', 'death_year']] = profs_df['Sterfdatum'].str.split('-', expand=True)
    profs_df[['promotion_day', 'promotion_month', 'promotion_year']] = profs_df['Datum'].str.split('-', expand=True)
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

    # Fix years
    for idx, row in profs_df.iterrows():
        value = len(str(row['birth_day']))
        if value > 2:
            profs_df.loc[idx, 'birth_year'] = row['birth_day']
            profs_df.loc[idx, 'birth_day'] = None
        value = len(str(row['death_day']))
        if value > 2:
            profs_df.loc[idx, 'death_year'] = row['death_day']
            profs_df.loc[idx, 'death_day'] = None
        value = len(str(row['promotion_day']))
        if value > 2:
            profs_df.loc[idx, 'promotion_year'] = row['promotion_day']
            profs_df.loc[idx, 'promotion_day'] = None
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

    job_1 = profs_df[['Aanstelling I', 'Vakgebied I', 'Leeropdracht I', 'Oratie/openbare les', 'Faculteit I', 'Reden I',
                      'Bijzonderheden I', 'aan1y', 'or1y', 'ed1y']]
    job_1 = job_1.rename(
        columns={'Aanstelling I': 'appointment_type', 'Vakgebied I': 'subject_area', 'Leeropdracht I': 'teaching',
                 'Oratie/openbare les': 'oration', 'Faculteit I': 'faculty', 'Reden I': 'reason',
                 'Bijzonderheden I': 'details', 'aan1y': 'appointment_year', 'or1y': 'oration_year',
                 'ed1y': 'end_year'})
    job_2 = profs_df[
        ['Aanstelling II', 'Vakgebied II', 'Leeropdracht II (Onderwijs of Vakgebied)',
         'Oratie/Openbare les II', 'Faculteit II', 'Reden II',
         'Bijzonderheden II', 'aan2y', 'or2y', 'ed2y']]
    job_2 = job_2.rename(
        columns={'Aanstelling II': 'appointment_type', 'Vakgebied II': 'subject_area',
                 'Leeropdracht II (Onderwijs of Vakgebied)': 'teaching',
                 'Oratie/Openbare les II': 'oration', 'Faculteit II': 'faculty', 'Reden II': 'reason',
                 'Bijzonderheden II': 'details', 'aan2y': 'appointment_year', 'or2y': 'oration_year',
                 'ed2y': 'end_year'})
    job_3 = profs_df[
        ['Aanstelling III', 'Vakgebied III', 'Leeropdracht III (Onderwijs of Vakgebied)',
         'Oratie/openbare les III', 'Faculteit III', 'Reden III',
         'Bijzonderheden III', 'aan3y', 'or3y', 'ed3y']]
    job_3 = job_3.rename(
        columns={'Aanstelling III': 'appointment_type', 'Vakgebied III': 'subject_area',
                 'Leeropdracht III (Onderwijs of Vakgebied)': 'teaching',
                 'Oratie/openbare les III': 'oration', 'Faculteit III': 'faculty', 'Reden III': 'reason',
                 'Bijzonderheden III': 'details', 'aan3y': 'appointment_year', 'or3y': 'oration_year',
                 'ed3y': 'end_year'})
    job_4 = profs_df[
        ['Aanstelling IV', 'Vakgebied IV', 'Leeropdracht IV (Onderwijs of Vakgebied)',
         'Oratie/openbare les IV', 'Faculteit IV', 'Reden IV',
         'Bijzonderheden IV', 'aan4y', 'or4y', 'ed4y']]
    job_4 = job_4.rename(
        columns={'Aanstelling IV': 'appointment_type', 'Vakgebied IV': 'subject_area',
                 'Leeropdracht IV (Onderwijs of Vakgebied)': 'teaching',
                 'Oratie/openbare les IV': 'oration', 'Faculteit IV': 'faculty', 'Reden IV': 'reason',
                 'Bijzonderheden IV': 'details', 'aan4y': 'appointment_year', 'or4y': 'oration_year',
                 'ed4y': 'end_year'})

    all_jobs = pd.concat([job_1, job_2], axis=0)
    all_jobs = pd.concat([all_jobs, job_3], axis=0)
    all_jobs = pd.concat([all_jobs, job_4], axis=0)
    all_jobs = all_jobs.dropna(how='all')

    # Create centuries
    profs_df['birth_century'] = profs_df['birth_year'].astype(str).str[:2]
    profs_df['birth_century'] = profs_df['birth_century'].replace(['na', 'No'], '0')
    profs_df['birth_century'] = profs_df['birth_century'].astype(int) + 1
    profs_df['birth_century'] = profs_df['birth_century'].apply(lambda x: np.nan if x == 1 else x)
    profs_df['death_century'] = profs_df['death_year'].astype(str).str[:2]
    profs_df['death_century'] = profs_df['death_century'].replace(['na', 'No'], '0')
    profs_df['death_century'] = profs_df['death_century'].astype(int) + 1
    profs_df['death_century'] = profs_df['death_century'].apply(lambda x: np.nan if x == 1 else x)
    profs_df['promotion_century'] = profs_df['promotion_year'].astype(str).str[:2]
    profs_df['promotion_century'] = profs_df['promotion_century'].replace(['na', 'No'], '0')
    profs_df['promotion_century'] = profs_df['promotion_century'].astype(int) + 1
    profs_df['promotion_century'] = profs_df['promotion_century'].apply(lambda x: np.nan if x == 1 else x)
    profs_df['appointment_century'] = profs_df['aan1y'].astype(str).str[:2]
    profs_df['appointment_century'] = profs_df['appointment_century'].replace(['na', 'No'], '0')
    profs_df['appointment_century'] = profs_df['appointment_century'].astype(int) + 1
    profs_df['appointment_century'] = profs_df['appointment_century'].apply(lambda x: np.nan if x == 1 else x)
    profs_df['end_century'] = profs_df['ed1y'].astype(str).str[:2]
    profs_df['end_century'] = profs_df['end_century'].replace(['na', 'No'], '0')
    profs_df['end_century'] = profs_df['end_century'].astype(int) + 1
    profs_df['end_century'] = profs_df['end_century'].apply(lambda x: np.nan if x == 1 else x)
    all_jobs['appointment_century'] = all_jobs['appointment_year'].astype(str).str[:2]
    all_jobs['appointment_century'] = all_jobs['appointment_century'].replace(['na', 'No'], '0')
    all_jobs['appointment_century'] = all_jobs['appointment_century'].astype(int) + 1
    all_jobs['appointment_century'] = all_jobs['appointment_century'].apply(lambda x: np.nan if x == 1 else x)
    all_jobs['end_century'] = all_jobs['end_year'].astype(str).str[:2]
    all_jobs['end_century'] = all_jobs['end_century'].replace(['na', 'No'], '0')
    all_jobs['end_century'] = all_jobs['end_century'].astype(int) + 1
    all_jobs['end_century'] = all_jobs['end_century'].apply(lambda x: np.nan if x == 1 else x)

    temp_birth = profs_df.dropna(subset=['birth_year'])
    profsbirth_df = split_years(temp_birth.sort_values(by='birth_year'), 'birth_year')
    temp_death = profs_df.dropna(subset=['death_year'])
    profsdeath_df = split_years(temp_death.sort_values(by='death_year'), 'death_year')
    temp_promotion = profs_df.dropna(subset=['promotion_year'])
    profspromotion_df = split_years(temp_promotion.sort_values(by='promotion_year'), 'promotion_year')
    temp_aanstelling = all_jobs.dropna(subset=['appointment_year'])
    profsaanstelling_df = split_years(temp_aanstelling.sort_values(by='appointment_year'), 'appointment_year')
    temp_einde = all_jobs.dropna(subset=['end_year'])
    profseinde_df = split_years(temp_einde.sort_values(by='end_year'), 'end_year')

    all_jobs.to_excel('excelfiles/professors_all_jobs.xlsx', index=False)
    profs_df.to_excel('excelfiles/professors_data.xlsx', index=False)

    # Gender
    gender_df = create_value_counts_professor(profsbirth_df, 'gender', 'Geslacht', 'birth_year', 'birth_century')
    gender_df.to_excel('excelfiles/professors_gender.xlsx', index=False)

    # Title
    title_df = create_value_counts_professor(profsbirth_df, 'title', 'Titulatuur 1', 'birth_year', 'birth_century')
    title_df.to_excel('excelfiles/professors_title.xlsx', index=False)

    # Birth
    birth_df = create_value_counts_professor(profsbirth_df, 'birth', 'birth_year', 'birth_year', 'birth_century')
    birth_df.to_excel('excelfiles/professors_birth.xlsx', index=False)

    # Birthplace
    birthplace_df = create_value_counts_professor(profsbirth_df, 'birth place', 'Geboorteplaats', 'birth_year',
                                                  'birth_century')
    birthplace_df.to_excel('excelfiles/professors_birth_place.xlsx', index=False)

    # Birthcountry
    birthcountry_df = create_value_counts_professor(profsbirth_df, 'country', 'Geboorteland', 'birth_year',
                                                    'birth_century')
    birthcountry_df = add_country_info(birthcountry_df)
    birthcountry_df.to_excel('excelfiles/professors_birth_country.xlsx', index=False)

    # Death
    death_df = create_value_counts_professor(profsdeath_df, 'death', 'death_year', 'death_year', 'death_century')
    death_df.to_excel('excelfiles/professors_death.xlsx', index=False)

    # Deathplace
    deathplace_df = create_value_counts_professor(profsdeath_df, 'death place', 'Sterfplaats', 'death_year',
                                                  'death_century')
    deathplace_df.to_excel('excelfiles/professors_death_place.xlsx', index=False)

    # Deathcountry
    deathcountry_df = create_value_counts_professor(profsdeath_df, 'country', 'Land van overlijden', 'death_year',
                                                    'death_century')
    deathcountry_df = add_country_info(deathcountry_df)
    deathcountry_df.to_excel('excelfiles/professors_death_country.xlsx', index=False)

    # promotion
    promotion_df = create_value_counts_professor(profspromotion_df, 'promotion', 'Datum', 'promotion_year',
                                                 'promotion_century')
    promotion_df.to_excel('excelfiles/professors_promotion.xlsx', index=False)

    # Promotion type
    promotiontype_df = create_value_counts_professor(profspromotion_df, 'promotion type', 'Examentype',
                                                     'promotion_year', 'promotion_century')
    promotiontype_df.to_excel('excelfiles/professors_promotion_type.xlsx', index=False)

    # Promotionplace
    promotionplace_df = create_value_counts_professor(profspromotion_df, 'promotion place', 'Instelling',
                                                      'promotion_year', 'promotion_century')
    promotionplace_df.to_excel('excelfiles/professors_promotion_place.xlsx', index=False)

    # Appointment
    appointment_df = create_value_counts_professor(profsaanstelling_df, 'appointment', 'appointment_year',
                                                   'appointment_year', 'appointment_century')
    appointment_df.to_excel('excelfiles/professors_appointment.xlsx', index=False)

    # Job
    job_df = create_value_counts_professor(profsaanstelling_df, 'job', 'appointment_type', 'appointment_year',
                                           'appointment_century')
    job_df.to_excel('excelfiles/professors_job.xlsx', index=False)

    # Subject area
    subject_df = create_value_counts_professor(profsaanstelling_df, 'subject area', 'subject_area', 'appointment_year',
                                               'appointment_century')
    subject_df.to_excel('excelfiles/professors_subject.xlsx', index=False)

    # Faculty
    faculty_df = create_value_counts_professor(profsaanstelling_df, 'faculty', 'faculty', 'appointment_year',
                                               'appointment_century')
    faculty_df.to_excel('excelfiles/professors_faculty.xlsx', index=False)

    # End
    end_df = create_value_counts_professor(profseinde_df, 'end of employment', 'end_year', 'end_year',
                                           'end_century')
    end_df.to_excel('excelfiles/professors_end.xlsx', index=False)

    # Profs information
    individual_profs_df = profs_df[['Voornamen', 'Achternaam', 'Geslacht', 'Titulatuur 1', 'Geboortedatum',
                                    'birth_year', 'Geboorteplaats', 'Geboorteland', 'Sterfdatum', 'death_year',
                                    'Sterfplaats', 'Land van overlijden', 'Examentype', 'Instelling', 'Datum',
                                    'promotion_year', 'Proefschrift', 'Aanstelling I', 'aan1y', 'Vakgebied I',
                                    'Datum aanstelling I', 'Ambtsaanvaarding I', 'Leeropdracht I', 'Datum oratie I',
                                    'Oratie/openbare les', 'Faculteit I', 'Einde dienstverband I', 'ed1y', 'Reden I',
                                    'Bijzonderheden I']]
    individual_profs_df = individual_profs_df.rename(columns={'Voornamen': 'First name', 'Achternaam': 'Last name',
                                                              'Geslacht': 'Gender', 'Titulatuur 1': 'Title',
                                                              'Geboortedatum': 'Birth date',
                                                              'birth_year': 'Birth year',
                                                              'Geboorteplaats': 'Birth place',
                                                              'Geboorteland': 'Birth country',
                                                              'Sterfdatum': 'Death date',
                                                              'death_year': 'Death year',
                                                              'Sterfplaats': 'Death place',
                                                              'Land van overlijden': 'Death country',
                                                              'Examentype': 'Promotion',
                                                              'Instelling': 'Promotion place',
                                                              'Datum': 'Promotion date',
                                                              'promotion_year': 'Promotion year',
                                                              'Proefschrift': 'Thesis', 'Aanstelling I': 'Job',
                                                              'Vakgebied I': 'Subject area',
                                                              'Datum aanstelling I': 'Appointment date',
                                                              'aan1y': 'Appointment year',
                                                              'Leeropdracht I': 'Teaching',
                                                              'Datum oratie I': 'Oration date',
                                                              'Oratie/openbare les': 'Oration',
                                                              'Faculteit I': 'Faculty',
                                                              'Einde dienstverband I': 'End of employment',
                                                              'ed1y': 'End of employmnet year',
                                                              'Reden I': 'Reason',
                                                              'Bijzonderheden I': 'Details'})
    individual_profs_df['Rating'] = 3
    individual_profs_df['Rating'] = individual_profs_df['Rating'].apply(lambda x: '⭐⭐⭐' if x >= 3 else ('⭐⭐' if x >= 2
                                                                                                        else (
        '⭐' if x >= 1 else '')))
    individual_profs_df.to_excel('excelfiles/professors_individual.xlsx', index=False)
    return print("Professor data cleaned")


def clean_student_data():
    students_df = pd.read_excel('excelfiles/Alle inschrijvingen 1575-1812.xlsx')
    students_df = students_df.replace(['nl'], 'Nederland')
    students_df = students_df.replace(['NL'], 'Nederland')
    students_df = students_df.replace(['Z-NL'], 'Belgie')
    students_df = students_df.replace(['Arabie'], 'Iran')
    students_df = students_df.replace(['Maltha'], 'Malta')
    students_df = students_df.replace(['Osmaanse rijk'], 'Turkije')
    students_df = students_df[students_df.LAND != '-']
    students_df = students_df[students_df.LAND != '?']
    students_df['LEEFTIJD_as'] = students_df['LEEFTIJD_as'].replace([999], 0)
    columns = ['DATUMINDAG_as', 'DATUMINMND_as', 'DATUMJAAR_as']
    students_df['start_date'] = students_df[columns].apply(lambda x: '-'.join(x.values.astype(str)), axis='columns')
    students_df['Rating'] = 3
    students_df['Rating'] = students_df['Rating'].apply(lambda x: '⭐⭐⭐' if x >= 3 else ('⭐⭐' if x >= 2 else
                                                                                        ('⭐' if x >= 1 else '')))
    students_df.to_excel('excelfiles/students_data.xlsx', index=False)

    # Split dataframe
    students2_df = split_years(students_df, 'DATUMJAAR_as')

    # Century
    century_df = create_value_counts_students(students2_df, 'century', 'EEUW')
    century_df.to_excel('excelfiles/students_century.xlsx', index=False)

    # Year
    year_df = create_value_counts_students(students2_df, 'year', 'DATUMJAAR_as')
    year_df.to_excel('excelfiles/students_years.xlsx', index=False)

    # Country
    country_df = create_value_counts_students(students2_df, 'country', 'LAND')
    country_df.loc[country_df.country == 'Nederland', 'iso_alpha'] = 'NLD'
    country_df.loc[country_df.country == 'Nederland', 'lat'] = '52.132633'
    country_df.loc[country_df.country == 'Nederland', 'lon'] = '5.291266'
    country_df.loc[country_df.country == 'Belgie', 'iso_alpha'] = 'BEL'
    country_df.loc[country_df.country == 'Belgie', 'lat'] = '50.503887'
    country_df.loc[country_df.country == 'Belgie', 'lon'] = '4.469936'
    country_df.loc[country_df.country == 'Duitsland', 'iso_alpha'] = 'DEU'
    country_df.loc[country_df.country == 'Duitsland', 'lat'] = '51.165691'
    country_df.loc[country_df.country == 'Duitsland', 'lon'] = '10.451526'
    country_df.loc[country_df.country == 'Britse eilanden', 'iso_alpha'] = 'GBR'
    country_df.loc[country_df.country == 'Britse eilanden', 'lat'] = '55.378051'
    country_df.loc[country_df.country == 'Britse eilanden', 'lon'] = '-3.435973'
    country_df.loc[country_df.country == 'Frankrijk', 'iso_alpha'] = 'FRA'
    country_df.loc[country_df.country == 'Frankrijk', 'lat'] = '46.227638'
    country_df.loc[country_df.country == 'Frankrijk', 'lon'] = '2.213749'
    country_df.loc[country_df.country == 'Denemarken', 'iso_alpha'] = 'DNK'
    country_df.loc[country_df.country == 'Denemarken', 'lat'] = '56.26392'
    country_df.loc[country_df.country == 'Denemarken', 'lon'] = '9.501785'
    country_df.loc[country_df.country == 'Polen', 'iso_alpha'] = 'POL'
    country_df.loc[country_df.country == 'Polen', 'lat'] = '51.919438'
    country_df.loc[country_df.country == 'Polen', 'lon'] = '19.145136'
    country_df.loc[country_df.country == 'Zwitserland', 'iso_alpha'] = 'CHE'
    country_df.loc[country_df.country == 'Zwitserland', 'lat'] = '49.817492'
    country_df.loc[country_df.country == 'Zwitserland', 'lon'] = '15.472962'
    country_df.loc[country_df.country == 'Italie', 'iso_alpha'] = 'ITA'
    country_df.loc[country_df.country == 'Italie', 'lat'] = '41.87194'
    country_df.loc[country_df.country == 'Italie', 'lon'] = '12.56738'
    country_df.loc[country_df.country == 'Zweden', 'iso_alpha'] = 'SWE'
    country_df.loc[country_df.country == 'Zweden', 'lat'] = '60.128161'
    country_df.loc[country_df.country == 'Zweden', 'lon'] = '18.643501'
    country_df.loc[country_df.country == 'Hongarije', 'iso_alpha'] = 'HUN'
    country_df.loc[country_df.country == 'Hongarije', 'lat'] = '47.162494'
    country_df.loc[country_df.country == 'Hongarije', 'lon'] = '19.503304'
    country_df.loc[country_df.country == 'Noorwegen', 'iso_alpha'] = 'NOR'
    country_df.loc[country_df.country == 'Noorwegen', 'lat'] = '60.472024'
    country_df.loc[country_df.country == 'Noorwegen', 'lon'] = '8.468946'
    country_df.loc[country_df.country == 'Rusland', 'iso_alpha'] = 'RUS'
    country_df.loc[country_df.country == 'Rusland', 'lat'] = '61.52401'
    country_df.loc[country_df.country == 'Rusland', 'lon'] = '105.318756'
    country_df.loc[country_df.country == 'Portugal', 'iso_alpha'] = 'PRT'
    country_df.loc[country_df.country == 'Portugal', 'lat'] = '39.399872'
    country_df.loc[country_df.country == 'Portugal', 'lon'] = '-8.224454'
    country_df.loc[country_df.country == 'Finland', 'iso_alpha'] = 'FIN'
    country_df.loc[country_df.country == 'Finland', 'lat'] = '61.92411'
    country_df.loc[country_df.country == 'Finland', 'lon'] = '25.748151'
    country_df.loc[country_df.country == 'Spanje', 'iso_alpha'] = 'ESP'
    country_df.loc[country_df.country == 'Spanje', 'lat'] = '40.463667'
    country_df.loc[country_df.country == 'Spanje', 'lon'] = '-3.74922'
    country_df.loc[country_df.country == 'Afrika', 'iso_alpha'] = 'MAR'
    country_df.loc[country_df.country == 'Afrika', 'lat'] = '31.791702'
    country_df.loc[country_df.country == 'Afrika', 'lon'] = '-7.09262'
    country_df.loc[country_df.country == 'IJsland', 'iso_alpha'] = 'ISL'
    country_df.loc[country_df.country == 'IJsland', 'lat'] = '64.963051'
    country_df.loc[country_df.country == 'IJsland', 'lon'] = '-19.020835'
    country_df.loc[country_df.country == 'Arabie', 'iso_alpha'] = 'IRN'
    country_df.loc[country_df.country == 'Arabie', 'lat'] = '32.427908'
    country_df.loc[country_df.country == 'Arabie', 'lon'] = '53.688046'
    country_df.loc[country_df.country == 'Maltha', 'iso_alpha'] = 'MLT'
    country_df.loc[country_df.country == 'Maltha', 'lat'] = '35.937496'
    country_df.loc[country_df.country == 'Maltha', 'lon'] = '14.375416'
    country_df.loc[country_df.country == 'Osmaanse rijk', 'iso_alpha'] = 'TUR'
    country_df.loc[country_df.country == 'Osmaanse rijk', 'lat'] = '38.963745'
    country_df.loc[country_df.country == 'Osmaanse rijk', 'lon'] = '35.243322'
    country_df.to_excel('excelfiles/students_country.xlsx', index=False)

    # City
    city_df = create_value_counts_students(students2_df, 'city', 'VERT_PLAATS')
    city_df.to_excel('excelfiles/students_city.xlsx', index=False)

    # Region
    region_df = create_value_counts_students(students2_df, 'region', 'REGIO2_WERELDDEEL')
    region_df.to_excel('excelfiles/students_region.xlsx', index=False)

    # Age
    age_df = create_value_counts_students(students2_df, 'age', 'LEEFTIJD_as')
    age_df.to_excel('excelfiles/students_age.xlsx', index=False)

    # Faculty
    fac_df = create_value_counts_students(students2_df, 'faculty', 'VERT_FAC')
    fac_df.to_excel('excelfiles/students_faculty.xlsx', index=False)

    # Extra
    extra_df = create_value_counts_students(students2_df, 'extra', 'VERT_AANVULLING')
    extra_df.to_excel('excelfiles/students_extra.xlsx', index=False)

    # Gratis
    gratis_df = create_value_counts_students(students2_df, 'gratis', 'GRATIS_as')
    gratis_df.to_excel('excelfiles/students_gratis.xlsx', index=False)

    # Status
    status_df = create_value_counts_students(students2_df, 'status', 'STATUS_INGESCHREVENE')
    status_df = status_df[status_df.status != 'Edele ?']
    status_df = status_df[status_df.status != 'Controleer']
    status_df = status_df[status_df.status != 'Edele ? C nog']
    status_df.to_excel('excelfiles/students_status.xlsx', index=False)

    # Job
    job_df = create_value_counts_students(students2_df, 'job', 'BEROEP_INGESCHREVENE')
    job_df.to_excel('excelfiles/students_job.xlsx', index=False)

    # Religion
    rel_df = create_value_counts_students(students2_df, 'religion', 'RELIGIE_INGESCHREVENE')
    rel_df.to_excel('excelfiles/students_rel.xlsx', index=False)

    # Previous Enrollments
    previous_df = create_value_counts_students(students2_df, 'previous', 'INS_KEER')
    previous_df.to_excel('excelfiles/students_previous.xlsx', index=False)

    # Individual information
    individual_df = students_df[
        ['VOORNAAM_as', 'ACHTERNAAM_as', 'DATUMINDAG_as', 'DATUMINMND_as', 'DATUMJAAR_as', 'EEUW',
         'VERT_PLAATS', 'LAND', 'REGIO2_WERELDDEEL', 'LEEFTIJD_as', 'GEB_JAAR', 'VERT_FAC',
         'VERT_AANVULLING', 'Bijzonder', 'GRATIS_as', 'STATUS_INGESCHREVENE', 'BEROEP_INGESCHREVENE'
            , 'RELIGIE_INGESCHREVENE', 'INS_KEER', 'INS_EERDER', 'INS_FAC_EERDER', 'INS_FAC_ORIGINEEL',
         'Rating']
    ]
    individual_df = individual_df.rename(columns={'VOORNAAM_as': 'First name', 'ACHTERNAAM_as': 'Last name',
                                                  'DATUMINDAG_as': 'Enrollment day',
                                                  'DATUMINMND_as': 'Enrollment month',
                                                  'DATUMJAAR_as': 'Enrollment year', 'EEUW': 'Century',
                                                  'VERT_PLAATS': 'City', 'LAND': 'Country',
                                                  'REGIO2_WERELDDEEL': 'Region',
                                                  'LEEFTIJD_as': 'Enrollment age', 'GEB_JAAR': 'Birth year',
                                                  'VERT_FAC': 'Faculty', 'VERT_AANVULLING': 'Extra',
                                                  'Bijzonder': 'Remark',
                                                  'GRATIS_as': 'Honor', 'STATUS_INGESCHREVENE': 'Royal title',
                                                  'BEROEP_INGESCHREVENE': 'Job', 'RELIGIE_INGESCHREVENE': 'Religion',
                                                  'INS_KEER': 'Enrollments', 'INS_EERDER': 'Previous enrollment',
                                                  'INS_FAC_EERDER': 'Previous faculty',
                                                  'INS_FAC_ORIGINEEL': 'Original faculty'})
    individual_df.to_excel('excelfiles/students_individual.xlsx', index=False)
    return print("Students data cleaned")


def clean_recmag_data():
    recmag_df = pd.read_csv('excelfiles/recmag_v1.csv')
    recmag_df.to_excel('excelfiles/recmag_data.xlsx', index=False)
    return print("Recmag data cleaned")


def check_missing_values():
    profs_df = pd.read_excel('excelfiles/Hoogleraren.xlsx')
    students_df = pd.read_excel('excelfiles/Alle inschrijvingen 1575-1812.xlsx')

    prof_number = 1181
    prof_columns = ['Nobelprijs', 'Achternaam', 'Voornamen', 'Geslacht', 'Titulatuur 1', 'Geboortedatum',
                    'Geboorteplaats',
                    'Geboorteland', 'Sterfdatum', 'Sterfplaats', 'Land van overlijden', 'Examentype', 'Instelling',
                    'Datum', 'Proefschrift', 'Aanstelling I', 'Vakgebied I', 'Datum aanstelling I', 'Leeropdracht I',
                    'Faculteit I', 'Einde dienstverband I', 'Reden I', 'Bijzonderheden I']
    student_number = 61269
    student_columns = ['VOORNAAM_as', 'ACHTERNAAM_as', 'VERT_PLAATS', 'LAND', 'REGIO2_WERELDDEEL', 'GEB_JAAR',
                       'VERT_AANVULLING', 'Bijzonder', 'GRATIS_as', 'STATUS_INGESCHREVENE', 'BEROEP_INGESCHREVENE',
                       'RELIGIE_INGESCHREVENE', 'DATUMJAAR_as', 'LEEFTIJD_as', 'INS_KEER', 'INS_EERDER',
                       'INS_FAC_EERDER']

    for column in prof_columns:
        number = profs_df[column].isnull().sum()
        print(column)
        print(number)
        print(number / prof_number)

    for column in student_columns:
        number = students_df[column].isnull().sum()
        print(column)
        print(number)
        print(number / student_number)


clean_professor_data()
clean_student_data()
clean_recmag_data()
check_missing_values()
