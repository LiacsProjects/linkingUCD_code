from datetime import datetime

import dateutil.parser

import database
import numpy as np
import pandas as pd
import time
import warnings
import parsedatetime
# import dateutil.parser as dparser

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
    elif date_string is np.nan:
        return np.nan

    # TODO: Accept incomplete dates, i.e. 1980, 1908-01, etc.
    # TODO: Write to file and manually change incorrect dates

    # Check if date is according to yyyy-mm-dd format
    try:
        d = datetime.strptime(date_string, "%Y-%m-%d")
        return d
    except ValueError:
        pass

    # Check if date is according to dd-mm-yyyy format and convert to yyyy-mm-dd format
    try:
        d = datetime.strptime(date_string, '%d-%m-%Y')
        return d.strftime('%Y-%m-%d')
    except ValueError:
        pass

    # print(date_string)
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
def convertTypeToID(conn, textual_types, table_name):
    """
    Converts list/pd series of "textual" types to corresponding IDs
    :param conn: database connection
    :param textual_types: list or pd series containing textual types
    :param table_name: name of type table to retrieve IDs from
    :return: list IDs in the same order as the input
    """
    IDs = []
    type_df = conn.selectTypeTable(table_name)
    forbidden_types = [None, '-', '?']
    for text in textual_types:
        if text in forbidden_types:
            IDs.append(None)
            continue
            # Connect type name from excel to TypeID
        for typeID, typeText in type_df.itertuples(index=False):
            if text.title().strip().__eq__(typeText):
                IDs.append(int(typeID))
                break
    return IDs


# Initiate typed tables
def initiateProfessorTypes(df):
    # Connect with database
    conn = database.Connection()
    profession = getTypesPerColumn(conn, "profession",
                                   pd.DataFrame(["University Employment", "University Guest", "Student"]))
    expertise = getTypesPerColumn(conn, "expertise",
                                  df[["Vakgebied I", "Vakgebied II", "Vakgebied III", "Vakgebied IV"]])
    faculty = getTypesPerColumn(conn, "faculty",
                                df[["Faculteit I", "Faculteit II", "Faculteit III", "Faculteit IV"]])
    location = getTypesPerColumn(conn, "location", pd.DataFrame(["Geboorteplaats", "Sterfplaats"]))
    person = getTypesPerColumn(conn, "person", pd.DataFrame(["Professor", "Student"]))
    position = getTypesPerColumn(conn, "position",
                                 df[["Aanstelling I", "Aanstelling II", "Aanstelling III", "Aanstelling IV"]])
    source = getTypesPerColumn(conn, "source", pd.DataFrame(["Excel Hoogleraren"]))
    if source is not None:
        source.insert(loc=2, column="Rating", value=3)

    conn.insert("type_of_profession", ["ProfessionID", "ProfessionType"], profession, True)
    conn.insert("type_of_expertise", ["ExpertiseID", "ExpertiseType"], expertise, True)
    conn.insert("type_of_faculty", ["FacultyID", "FacultyType"], faculty, True)
    conn.insert("type_of_location", ["LocationID", "LocationType"], location, True)
    conn.insert("type_of_person", ["PersonID", "PersonType"], person, True)
    conn.insert("type_of_position", ["PositionID", "PositionType"], position, True)
    conn.insert("type_of_source", ["SourceID", "SourceType", "Rating"], source, True)

    # Commit and close database connection
    del conn


# Process and insert professor data
def insertProfessors(df):
    # Connect with database
    conn = database.Connection()

    # Create and insert person dataframe
    maxID = conn.getPersonMaxID()
    if maxID is None:
        maxID = 0
    maxID += 1
    # Handle: http://hdl.handle.net/1887.1/item:[nummer]
    person_df = df[["Voornamen", "Achternaam", "Achternaam", "Roepnaam", "Geslacht", "Geboorteland", "Handle", "NAVG"]]
    person_df.insert(loc=0, column="PersonID", value=range(maxID, maxID + len(person_df)))
    person_df.insert(loc=1, column="TypeOfPerson", value=convertTypeToID(conn, ["Professor"], "type_of_person")[0])
    person_attributes = ["PersonID", "TypeOfPerson", "FirstName", "LastName", "FamilyName", "Nickname", "Gender", "Nationality", "Handles", "AVG"]
    conn.insert("person", person_attributes, person_df.replace({np.nan: None}), True)

    # Create and insert location dataframe
    birth_loc_df = df[["Geboorteland", "Geboorteplaats", "geboortedatum"]]
    # Filter for empty rows in advance
    birth_loc_df = birth_loc_df[
        birth_loc_df["Geboorteland"].notna() | birth_loc_df["Geboorteplaats"].notna() | birth_loc_df[
            "geboortedatum"].notna()]
    birth_loc_df.insert(loc=0, column="LocationID", value=None)  # For autoincrement
    birth_loc_df.insert(loc=1, column="TypeOfLocation", value=convertTypeToID(conn, ["Geboorteplaats"], "type_of_location")[0])  # Place of birth ID
    birth_loc_df.insert(loc=5, column="EndDate", value=df["geboortedatum"])
    birth_loc_df.insert(loc=6, column="PersonID", value=person_df["PersonID"])
    location_attributes = ["LocationID", "TypeOfLocation", "Country", "City", "StartDate", "EndDate", "PersonID_location"]
    conn.insert("location", location_attributes, birth_loc_df.replace({np.nan: None}), True)
    # conn.insertMany("location", birth_loc_df.replace({np.nan: None}))

    death_loc_df = df[["Land van overlijden", "Sterfplaats", "Sterfdatum"]]
    # Filter for empty rows in advance
    death_loc_df = death_loc_df[
        death_loc_df["Land van overlijden"].notna() | death_loc_df["Sterfplaats"].notna() | death_loc_df[
            "Sterfdatum"].notna()]
    death_loc_df.insert(loc=0, column="LocationID", value=None)
    death_loc_df.insert(loc=1, column="TypeOfLocation", value=convertTypeToID(conn, ["Sterfplaats"], "type_of_location")[0])  # Place of death ID
    death_loc_df.insert(loc=5, column="EndDate", value=df["geboortedatum"])
    death_loc_df.insert(loc=6, column="PersonID", value=person_df["PersonID"])
    conn.insert("location", location_attributes, death_loc_df.replace({np.nan: None}), True)
    # conn.insertMany("location", death_loc_df.replace({np.nan: None}))

    # Create and insert profession dataframe
    # TODO: add Promotion(type/place/date) & Thesis
    """
    Promotion:
        - Type = Examentype
        - Place = Instelling
        - Date = (N)Datum
    Thesis = Proefschrift
    """
    periods = ['I', 'II', 'III', 'IV']
    for period in periods:
        period_df = df[['Datum aanstelling ' + period, 'Einde dienstverband ' + period]].replace({np.nan: None})
        period_df.insert(loc=0, column="ProfessionID", value=None)
        period_df.insert(loc=1, column="TypeOfProfession",
                         value=convertTypeToID(conn, ["University Employment"], "type_of_profession")[0])
        period_df.insert(loc=2, column="TypeOfPosition",
                         value=convertTypeToID(conn, df['Aanstelling ' + period], 'type_of_position'))
        period_df.insert(loc=3, column="TypeOfExpertise",
                         value=convertTypeToID(conn, df['Vakgebied ' + period], 'type_of_expertise'))
        period_df.insert(loc=4, column="TypeOfFaculty",
                         value=convertTypeToID(conn, df['Faculteit ' + period], 'type_of_faculty'))
        period_df.insert(loc=7, column="PersonID", value=person_df["PersonID"])

        # Filter entries to exclude empty professions
        period_df = period_df[
            (period_df['Datum aanstelling ' + period].notna()) | (period_df['TypeOfExpertise'].notna()) | (
                period_df['TypeOfPosition'].notna())]
        profession_attributes = ["ProfessionID", "TypeOfProfession", "TypeOfPosition", "TypeOfExpertise", "TypeOfFaculty", "StartDate", "EndDate", "PersonID_profession"]
        conn.insert("profession", profession_attributes, period_df.replace({np.nan: None}), True)

    # Commit and close database connection
    del conn


# initiateStudentTypes
def initiateStudentTypes(df):
    # Connect with database
    conn = database.Connection()

    person = getTypesPerColumn(conn, "person", pd.DataFrame(["Student"]))
    faculty = getTypesPerColumn(conn, "faculty", df[['VERT FAC']])
    position = getTypesPerColumn(conn, "position", pd.DataFrame(["Student"]))
    source = getTypesPerColumn(conn, "source", pd.DataFrame(["Excel Studenten 1575-1812"]))
    if source is not None:
        source.insert(loc=2, column="Rating", value=3)

    conn.insert("type_of_person", ["PersonID", "PersonType"], person, True)
    conn.insert("type_of_faculty", ["FacultyID", "FacultyType"], faculty, True)
    conn.insert("type_of_position", ["PositionID", "PositionType"], position, True)
    conn.insert("type_of_source", ["SourceID", "SourceType", "Rating"], source, True)

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
    person_df = df[["VN standaard", "AN standaard", "AN standaard", "LAND", "RELIGIE INGESCHREVENE", "STATUS INGESCHREVENE"]]
    person_df.insert(loc=0, column="PersonID", value=range(maxID, maxID + len(person_df)))
    person_df.insert(loc=1, column="TypeOfPerson", value=convertTypeToID(conn, ["Student"], "type_of_person")[0])
    person_df.insert(loc=8, column="AVG", value="VRIJ")
    person_attributes = ["PersonID", "TypeOfPerson", "FirstName", "LastName", "FamilyName", "Nationality", "Religion", "Status", "AVG"]
    conn.insert("person", person_attributes, person_df.replace({np.nan: None}), True)
    # conn.insertMany("person", person_df.replace({np.nan: None}))

    # TODO: insert PLAATS as if VERT PLAATS is NULL
    #  Do this for all "VERT" columns
    # Create and insert location dataframe
    birth_loc_df = df[["LAND", "VERT PLAATS", "REGIO2 WERELDDEEL"]].replace({np.nan: None})
    birth_loc_df.insert(loc=0, column="LocationID", value=None)
    birth_loc_df.insert(loc=1, column="TypeOfLocation", value=convertTypeToID(conn, ["Geboorteplaats"], "type_of_location")[0])
    # TODO: check if df['GEB JAAR'] != "None" can be done without intermediate step
    df['GEB JAAR'] = df['GEB JAAR'].astype(str)
    df['GEB JAAR'] = np.where(df['GEB JAAR'] == "None", np.nan, df['GEB JAAR'])
    df['GEB JAAR'] = np.where(df['GEB JAAR'] != np.nan, df['GEB JAAR'].str[:4] + "-01-01", df['GEB JAAR'])
    birth_loc_df.insert(loc=5, column="Geboortedatum", value=df['GEB JAAR'])
    birth_loc_df.insert(loc=6, column="EndDate", value=birth_loc_df["Geboortedatum"])
    birth_loc_df.insert(loc=7, column="PersonID", value=person_df["PersonID"])
    location_attributes = ["LocationID", "TypeOfLocation", "Country", "City", "Region", "StartDate", "EndDate", "PersonID_location"]
    conn.insert("location", location_attributes, birth_loc_df.replace({np.nan: None}), True)
    # conn.insertMany("location", birth_loc_df.replace({np.nan: None}))

    # Create and insert profession dataframe
    profession_attributes = ["ProfessionID", "TypeOfProfession", "TypeOfPosition", "TypeOfFaculty", "StartDate", "PersonID_profession"]
    profession_df = pd.DataFrame(columns=["PersonID"], data=person_df["PersonID"])
    profession_df.insert(loc=0, column="ProfessionID", value=None)
    profession_df.insert(loc=1, column="TypeOfProfession", value=convertTypeToID(conn, ["Student"], "type_of_profession")[0])
    profession_df.insert(loc=2, column="TypeOfPosition", value=convertTypeToID(conn, ["Student"], "type_of_position")[0])
    profession_df.insert(loc=3, column="TypeOfFaculty", value=convertTypeToID(conn, df['VERT FAC'], "type_of_faculty")[0])
    df['DATUMJAAR as'] = df['DATUMJAAR as'].map(str)
    df['DATUMINMND as'] = df['DATUMINMND as'].map(str)
    df['DATUMINDAG as'] = df['DATUMINDAG as'].map(str)
    registrationDate_df = pd.DataFrame(index=range(len(df)), columns=["reg"])
    registrationDate_df["reg"] = df['DATUMJAAR as'] + '-' + df['DATUMINMND as'] + '-' + df['DATUMINDAG as']
    registrationDate_df["reg"] = registrationDate_df["reg"].apply(is_date)
    profession_df.insert(loc=4, column="StartDate", value=registrationDate_df["reg"])
    # profession_df['StartDate'] = fixDates(registrationDate_df, [0], False)
    conn.insert("profession", profession_attributes, profession_df.replace({np.nan: None}), True)
    # conn.insertMany("profession", profession_df.replace({np.nan: None}))

    # Commit and close database connection
    del conn


# Hoogleraren - 'Hoogleraren all - Ariadne.xlsx'
def hoogleraren():
    # Handle: http://hdl.handle.net/1887.1/item:[nummer]
    # AVG: Alleen bij waarde "VRIJ" gebruiken
    # Convert excel file to Dataframe
    dateColumns = ["geboortedatum", "Sterfdatum", "Datum aanstelling I", "Datum aanstelling II",
                   "Datum aanstelling III", "Datum aanstelling IV", "Einde dienstverband I", "Einde dienstverband II",
                   "Einde dienstverband III", "Einde dienstverband IV"]
    # file_location = r"../data/Hoogleraren all - preprocessed.xlsx"
    file_location = r"../data/Hoogleraren all - Ariadne.xlsx"
    hoogleraren_df = pd.read_excel(file_location, engine='openpyxl', parse_dates=dateColumns).replace({np.nan: None})

    # TODO: improve date filter
    for column in dateColumns:
        hoogleraren_df[column] = hoogleraren_df[column].apply(is_date)

    hoogleraren_start = time.time()
    initiateProfessorTypes(hoogleraren_df)
    insertProfessors(hoogleraren_df)
    print(f"\"Professor\" adapter finished successfully in {round(time.time() - hoogleraren_start, 2)} seconds")


# Studenten - 'Alle inschrijvingen 1575-1812.xlsx'
def studenten():
    # Convert excel file to Dataframe
    file_location = r"../data/Alle inschrijvingen 1575-1812.xlsx"
    studenten_df = pd.read_excel(file_location, engine='openpyxl').replace({np.nan: None})

    student_start = time.time()
    initiateStudentTypes(studenten_df)
    insertStudents(studenten_df)
    print(f"\"Student 1575-1812\" adapter finished successfully in {round(time.time() - student_start, 2)} seconds")


def parseDate(df):
    # print(df_column.str.split('-', expand=True))
    for row in df.iterrows():
        print(row)
        print(row["Sterfdatum"].str.split('-', expand=True))
    # return df_column.str.split('-', expand=True)


# Function only for testing out stuff, can be removed if needed
def playground():
    dateColumns = ["geboortedatum", "Sterfdatum", "Datum aanstelling I", "Datum aanstelling II",
                   "Datum aanstelling III", "Datum aanstelling IV", "Einde dienstverband I", "Einde dienstverband II",
                   "Einde dienstverband III", "Einde dienstverband IV"]
    # file_location = r"../data/Hoogleraren all - preprocessed.xlsx"
    file_location = r"../data/Hoogleraren all - Ariadne.xlsx"
    df = pd.read_excel(file_location, engine='openpyxl', date_parser=dateutil.parser.parse, parse_dates=dateColumns).replace({np.nan: None})

    # print(len(df[df['Geboorteland'].isin(["Verenigd Koninkrijk"])]))
    start = time.time()
    print(df["geboortedatum"][0])
    print(dateutil.parser.parse('2015-1-19 ha', fuzzy_with_tokens=True, yearfirst=True))
    cal = parsedatetime.Calendar()
    # print(cal.parse('2014/2015'))
    time_struct, parse_status = cal.parse('ca. 2015')
    print(datetime(*time_struct[:6]))
    print(f"Program finished successfully in {time.time() - start} seconds")


# main
if __name__ == "__main__":
    # start = time.time()
    hoogleraren()
    studenten()
    # playground()

    # print(f"Program finished successfully in {round(time.time() - start, 2)} seconds")
