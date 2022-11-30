from datetime import datetime
import database
import numpy as np
import pandas as pd
import time
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)


# Fix dates that do not match the format and add to new df column
# If save_raw is True, raw value of "wrong" date will be saved in a new column
# Note: some not easily fixable dates (i.e. "1885-03-27, met ingang 1885-04-01") are ignored and discarded
# TODO: to be replaced by improved version
# TODO 2: remove function when when single 'date' attribute in DB model is replaced by 'year', 'month' and 'day'
def fixDates(df, columns, save_raw):
    df = df.replace({np.nan: None})
    if not save_raw:
        for column in columns:
            for date in df[column]:
                if date is None:
                    continue
                # date = "".join(c for c in date if c.isdecimal() or c is '-')
                if type(date) is float:
                    # print("Float", date)
                    date = str(int(date))
                    # print(date)
                date = date.strip()
                # print(date)
                if len(date) == 4 and date.isdigit():
                    df = df.replace(date, date + "-01-01")
                    continue
                elif len(date) == 7 and date[0:4].isdigit() and date[5:].isdigit():
                    try:
                        datetime.strptime(date, "%Y-%m")
                        df = df.replace(date, date + "-01")
                    except ValueError:
                        df = df.replace(date, None)
                    continue
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    # print(date)
                except ValueError:
                    # print(date)
                    df = df.replace(date, None)
    return df


# Return date if date is according to format, else return None
def is_date(date_string):
    if date_string is None:
        return None

    if date_string is np.nan:
        return np.nan

    # Check if date is according to yyyy-mm-dd format
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return date_string
    except ValueError:
        pass

    # Check if date is according to dd-mm-yyyy format and convert to yyyy-mm-dd format
    try:
        d = datetime.strptime(date_string, '%d-%m-%Y')
        return d.strftime('%Y-%m-%d')
    except ValueError:
        pass

    return None


# Returns sorted df of unique types (textual) per column from excel file
def getTypesPerColumn(conn, type_name, type_df):
    db_types_series = conn.selectTypeTable("type_of_" + type_name)[type_name.capitalize() + "Type"]
    new_types = pd.Series(data=[], dtype=str)

    # TODO add df.unique()
    for column in type_df:
        types_column = type_df[column].str.title().dropna().unique()
        # types_column = type_df[column].dropna().str.title()
        new_types = pd.concat([new_types, pd.Series(types_column)])
        # new_types.drop_duplicates(inplace=True)

    # Select only values that are in new_types but not in db_types_series to prevent duplicates in DB
    new_types = pd.Series(new_types.unique())
    new_types = new_types[~new_types.isin(db_types_series)]
    if len(new_types) == 0:
        return None
    # Create new df
    updated_types_df = pd.DataFrame(index=range(len(new_types)), columns=["None", "Types"])
    updated_types_df["None"] = None
    updated_types_df["Types"] = new_types.sort_values().values
    return updated_types_df


# Converts textual type to TypeID
def convertTypeToID(conn, df_column, table_name):
    IDs = []
    type_df = conn.selectTypeTable(table_name)
    forbidden_types = [None, '-', '?']
    for excel_type in df_column:
        if excel_type in forbidden_types:
            IDs.append(None)
            continue
            # Connect type name from excel to TypeID
        for typeID, typeText in type_df.itertuples(index=False):
            if excel_type.title().strip().__eq__(typeText):
                IDs.append(int(typeID))
                break
    return IDs


# Initiate typed tables
def initiateHooglerarenTypes(df):
    # Connect with database
    conn = database.Connection()
    engagement = getTypesPerColumn(conn, "engagement", pd.DataFrame(["Employment", "Guest", "Student"]))
    expertise = getTypesPerColumn(conn, "expertise",
                                  df[["Vakgebied I", "Vakgebied II", "Vakgebied III", "Vakgebied IV"]])
    faculty = getTypesPerColumn(conn, "faculty",
                                df[["Faculteit I", "Faculteit II", "Faculteit III", "Faculteit IV"]])
    location = getTypesPerColumn(conn, "location", pd.DataFrame(["Geboorteplaats", "Sterfplaats"]))
    person = getTypesPerColumn(conn, "person", pd.DataFrame(["Professor", "Student"]))
    position = getTypesPerColumn(conn, "position",
                                 df[["Aanstelling I", "Aanstelling II", "Aanstelling III", "Aanstelling IV"]])

    conn.insertMany("type_of_engagement", engagement)
    conn.insertMany("type_of_expertise", expertise)
    conn.insertMany("type_of_faculty", faculty)
    conn.insertMany("type_of_location", location)
    conn.insertMany("type_of_person", person)
    conn.insertMany("type_of_position", position)

    # Commit and close database connection
    del conn


# Process and insert professor data
def insertHoogleraren(df):
    # Connect with database
    conn = database.Connection()

    # Create and insert person dataframe
    maxID = conn.getPersonMaxID()
    if maxID is None:
        maxID = 0
    maxID += 1
    person_df = df[["Voornamen", "Achternaam", "Achternaam", "Roepnaam", "Geslacht", "Geboorteland"]]
    person_df.insert(loc=0, column="PersonID", value=range(maxID, maxID + len(person_df)))
    person_df.insert(loc=1, column="TypeOfPerson", value=1)  # Professor ID
    person_df.insert(loc=5, column="Affix", value=None)
    person_df.insert(loc=9, column="Religion", value=None)
    person_df.insert(loc=10, column="Status", value=None)
    person_df.insert(loc=11, column="Job", value=None)
    person_df.insert(loc=12, column="SourceName", value="Excel file hoogleraren")
    person_df.insert(loc=13, column="SourceRating", value=3)
    conn.insertMany("person", person_df.replace({np.nan: None}))

    # Create and insert location dataframe
    # TODO: resolve duplicate lines
    birth_location_df = df[["Geboorteland", "Geboorteplaats", "geboortedatum", "geboortedatum"]]
    birth_location_df.insert(loc=0, column="LocationID", value=None)
    birth_location_df.insert(loc=1, column="TypeOfLocation", value=1)  # Place of birth ID
    birth_location_df.insert(loc=4, column="Street", value=None)
    birth_location_df.insert(loc=5, column="HouseNumber", value=None)
    birth_location_df.insert(loc=6, column="Region", value=None)
    birth_location_df.insert(loc=9, column="SourceName", value="Excel file hoogleraren")
    birth_location_df.insert(loc=10, column="SourceRating", value=3)
    birth_location_df.insert(loc=11, column="PersonID", value=person_df["PersonID"])
    conn.insertMany("location", birth_location_df.replace({np.nan: None}))

    death_location_df = df[["Land van overlijden", "Sterfplaats", "Sterfdatum", "Sterfdatum"]]
    death_location_df.insert(loc=0, column="LocationID", value=None)
    death_location_df.insert(loc=1, column="TypeOfLocation", value=2)  # Place of death ID
    death_location_df.insert(loc=4, column="Street", value=None)
    death_location_df.insert(loc=5, column="HouseNumber", value=None)
    death_location_df.insert(loc=6, column="Region", value=None)
    death_location_df.insert(loc=9, column="SourceName", value="Excel file hoogleraren")
    death_location_df.insert(loc=10, column="SourceRating", value=3)
    death_location_df.insert(loc=11, column="PersonID", value=person_df["PersonID"])
    conn.insertMany("location", death_location_df.replace({np.nan: None}))

    # Create and insert engagement dataframe
    periods = ['I', 'II', 'III', 'IV']
    for period in periods:
        period_df = df[['Datum aanstelling ' + period, 'Einde dienstverband ' + period]].replace({np.nan: None})
        period_df.insert(loc=0, column="EngagementID", value=None)
        period_df.insert(loc=1, column="TypeOfEngagement", value=1)  # Employment ID
        period_df.insert(loc=2, column="TypeOfPosition",
                         value=convertTypeToID(conn, df['Aanstelling ' + period], 'type_of_position'))
        period_df.insert(loc=3, column="TypeOfExpertise",
                         value=convertTypeToID(conn, df['Vakgebied ' + period], 'type_of_expertise'))
        period_df.insert(loc=4, column="TypeOfFaculty",
                         value=convertTypeToID(conn, df['Faculteit ' + period], 'type_of_faculty'))
        period_df.insert(loc=7, column="SourceName", value="Excel file hoogleraren")
        period_df.insert(loc=8, column="SourceRating", value=3)
        period_df.insert(loc=9, column="PersonID", value=person_df["PersonID"])
        # Filter entries to exclude empty engagements
        period_df = period_df[
            (period_df['Datum aanstelling ' + period].notna()) | (period_df['TypeOfExpertise'].notna()) | (
                period_df['TypeOfPosition'].notna())]
        conn.insertMany("engagement", period_df.replace({np.nan: None}))

    # Commit and close database connection
    del conn


# initiateStudentTypes
def initiateStudentTypes(df):
    # Connect with database
    conn = database.Connection()

    faculty = getTypesPerColumn(conn, "faculty", df[['VERT_FAC']])
    position = getTypesPerColumn(conn, "person", pd.DataFrame(["Student"]))

    conn.insertMany("type_of_faculty", faculty)
    conn.insertMany("type_of_position", position)
    # Commit and close database connection
    del conn


# insertStudents
# TODO: update for model changes
def insertStudents(df):
    # Connect with database
    conn = database.Connection()

    # Create and insert person dataframe
    maxID = conn.getPersonMaxID()
    if maxID is None:
        maxID = 0
    maxID += 1
    # TODO:
    #  Convert "Bergh, van den" to "Bergh" and add "van den" as suffix
    #  VN_standaard: remove all after ','
    person_df = df[["VOORNAAM_as", "ACHTERNAAM_as", "LAND", "RELIGIE_INGESCHREVENE", "STATUS_INGESCHREVENE",
                    "BEROEP_INGESCHREVENE"]]
    person_df.insert(loc=0, column="PersonID", value=range(maxID, maxID + len(person_df)))
    person_df.insert(loc=3, column="Affix", value=None)
    person_df.insert(loc=4, column="Roepnaam", value=None)
    person_df.insert(loc=5, column="Geslacht", value=None)
    person_df.insert(loc=10, column="TypeOfPerson", value=2)  # Student ID
    conn.insertMany("person", person_df.replace({np.nan: None}))

    # TODO: insert PLAATS_as if VERT_PLAATS is NULL
    #  Do this for all "VERT" columns
    # Create and insert location dataframe
    birth_location_df = df[["LAND", "VERT_PLAATS", "REGIO2_WERELDDEEL"]].replace({np.nan: None})
    birth_location_df.insert(loc=0, column="LocationID", value=None)
    birth_location_df.insert(loc=1, column="TypeOfLocation", value=1)  # Place of birth ID
    # TODO: check if df['GEB_JAAR'] != "None" can be done without intermediate step
    df['GEB_JAAR'] = df['GEB_JAAR'].astype(str)
    df['GEB_JAAR'] = np.where(df['GEB_JAAR'] == "None", np.nan, df['GEB_JAAR'])
    df['GEB_JAAR'] = np.where(df['GEB_JAAR'] != np.nan, df['GEB_JAAR'].str[:4] + "-01-01", df['GEB_JAAR'])
    birth_location_df.insert(loc=5, column="Geboortedatum", value=df['GEB_JAAR'])
    birth_location_df.insert(loc=6, column="EndDate", value=birth_location_df["Geboortedatum"])
    birth_location_df.insert(loc=7, column="PersonID", value=person_df["PersonID"])
    conn.insertMany("location", birth_location_df.replace({np.nan: None}))

    # Create and insert engagement dataframe
    engagement_df = pd.DataFrame(
        columns=['EngagementID', 'TypeOfPosition', 'TypeOfExpertise', 'StartDate', 'EndDate', 'TypeOfFaculty',
                 'TypeOfEngagement', 'PersonID'])
    engagement_df['EngagementID'] = None
    student_df = pd.DataFrame(index=range(len(person_df)), columns=range(1))
    student_df[0] = "Student"
    engagement_df['TypeOfPosition'] = convertTypeToID(conn, student_df[0], 'type_of_position')
    engagement_df['TypeOfExpertise'] = None

    df['DATUMJAAR_as'] = df['DATUMJAAR_as'].map(str)
    df['DATUMINMND_as'] = df['DATUMINMND_as'].map(str)
    df['DATUMINDAG_as'] = df['DATUMINDAG_as'].map(str)
    registrationDate_df = pd.DataFrame(index=range(len(df)), columns=range(1))
    registrationDate_df[0] = df['DATUMJAAR_as'] + '-' + df['DATUMINMND_as'] + '-' + df['DATUMINDAG_as']

    engagement_df['StartDate'] = fixDates(registrationDate_df, [0], False)
    engagement_df['EndDate'] = None
    engagement_df['TypeOfFaculty'] = convertTypeToID(conn, df['VERT_FAC'], 'type_of_faculty')
    engagement_df['TypeOfEngagement'] = 3  # Student ID
    engagement_df['PersonID'] = person_df["PersonID"]
    conn.insertMany("engagement", engagement_df.replace({np.nan: None}))

    # Commit and close database connection
    del conn


# Hoogleraren - 'Hoogleraren all.xlsx'
def hoogleraren():
    # Convert excel file to Dataframe
    dateColumns = ["geboortedatum", "Sterfdatum", "Datum aanstelling I", "Datum aanstelling II",
                   "Datum aanstelling III", "Datum aanstelling IV", "Einde dienstverband I", "Einde dienstverband II",
                   "Einde dienstverband III", "Einde dienstverband IV"]
    file_location = r"data/Hoogleraren all - preprocessed.xlsx"
    hoogleraren_df = pd.read_excel(file_location, engine='openpyxl', parse_dates=dateColumns).replace({np.nan: None})

    # Filter dates
    for column in dateColumns:
        hoogleraren_df[column] = hoogleraren_df[column].apply(is_date)

    initiateHooglerarenTypes(hoogleraren_df)
    insertHoogleraren(hoogleraren_df)


# Studenten - 'Alle inschrijvingen 1575-1812.xlsx'
def studenten():
    # Convert excel file to Dataframe
    file_location = r"data/Alle inschrijvingen 1575-1812.xlsx"
    studenten_df = pd.read_excel(file_location, engine='openpyxl').replace({np.nan: None})

    initiateStudentTypes(studenten_df)
    insertStudents(studenten_df)


# Function only for testing out stuff, can be removed if needed
def testable():
    dateColumns = ["geboortedatum", "Sterfdatum", "Datum aanstelling I", "Datum aanstelling II",
                   "Datum aanstelling III", "Datum aanstelling IV", "Einde dienstverband I", "Einde dienstverband II",
                   "Einde dienstverband III", "Einde dienstverband IV"]
    file_location = r"data/Hoogleraren all - preprocessed.xlsx"
    df = pd.read_excel(file_location, engine='openpyxl', parse_dates=dateColumns).replace({np.nan: None})

    print(len(df[df['Geboorteland'].isin(["Verenigd Koninkrijk"])]))
    start = time.time()
    VK = ["Verenigd Koninkrijk, Engeland", "Verenigd Koninkrijk, Schotland", "Engeland", "Schotland", "Verenigd Koninkrijk, Noord-Ierland"]
    df['Geboorteland'] = df['Geboorteland'].where(~df['Geboorteland'].isin(VK), "Verenigd Koninkrijk")
    # for x in df.index:
    #     if df.loc[x, "Geboorteland"] in VK:
    #         df.loc[x, "Geboorteland"] = "Verenigd Koninkrijk"
    print(len(df[df['Geboorteland'].isin(["Verenigd Koninkrijk"])]))
    print(f"Program finished successfully in {time.time() - start} seconds")


# main
if __name__ == "__main__":
    # start = time.time()
    hoogleraren()
    # studenten()
    # testable()
    # print(f"Program finished successfully in {round(time.time() - start, 2)} seconds")
