from datetime import datetime

import dateutil.parser

import database
import numpy as np
import pandas as pd
import time
import warnings
import re

warnings.simplefilter(action='ignore', category=UserWarning)


def isYear(year):
    if year is None:
        return "0000"
    try:
        return datetime.strptime(year, "%Y").strftime("%Y")
    except ValueError:
        return "0000"


def isMonth(month):
    if month is None:
        return "00"
    try:
        return datetime.strptime(month, "%m").strftime("%m")
    except ValueError:
        return "00"


def isDay(day):
    if day is None:
        return "00"
    try:
        return datetime.strptime(day, "%d").strftime("%d")
    except ValueError:
        return "00"


def isDate(date):
    # Check if date is according to yyyy-mm-dd format
    try:
        return datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        pass

    # Check if date is turned around and correct it
    try:
        return datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
    except ValueError:
        pass

    return None


def checkDate(date):
    if date is None:
        return None
    elif date is np.nan:
        return np.nan

    new_date = isDate(date)
    if new_date is not None:
        return new_date

    # Match other formats based on regex in the order year, month and day
    year_pattern = r"(?P<year>\d{4})"
    month_pattern = r"(?:-(?P<month>\d{1,2}))"
    day_pattern = r"(?:-(?P<day>\d{1,2}))"

    match_date = re.search(rf'{year_pattern}(?:{month_pattern}{day_pattern}?)?', date)
    if match_date is not None:
        year = isYear(match_date.group('year'))
        month = isMonth(match_date.group('month'))
        day = isDay(match_date.group('day'))
        new_date = "-".join([year, month, day])
        if "00" not in new_date:  # Re-filter seemingly valid dates such as 1955-02-29 (1955 != leap year, so incorrect)
            return isDate(new_date)
        return new_date
    else:
        return None


# Returns sorted df of unique types (textual) per column from excel file
def getTypesPerColumn(conn, type_name, type_df):
    db_types_series = conn.selectTypeTable("type_of_" + type_name)[type_name.capitalize() + "Type"]
    new_types = pd.Series(data=[], dtype=str)

    for column in type_df:
        types_column = type_df[column].str.title().dropna().unique()
        new_types = pd.concat([new_types, pd.Series(types_column)])

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
    person_df.insert(loc=0, column="personPersonID", value=range(maxID, maxID + len(person_df)))
    person_df.insert(loc=1, column="TypeOfPerson", value=conn.convertTypeToID(["Professor"], "type_of_person")[0])
    person_attributes = ["personPersonID", "TypeOfPerson", "FirstName", "LastName", "FamilyName", "Nickname", "Gender",
                         "Nationality", "Handles", "AVG"]
    conn.insert("person", person_attributes, person_df.replace({np.nan: None}), True)

    # Create and insert location dataframe
    birth_loc_df = df[["Geboorteland", "Geboorteplaats", "geboortedatum"]]
    # Filter for empty rows in advance
    birth_loc_df = birth_loc_df[
        birth_loc_df["Geboorteland"].notna() | birth_loc_df["Geboorteplaats"].notna() | birth_loc_df[
            "geboortedatum"].notna()]
    birth_loc_df.insert(loc=0, column="LocationID", value=None)  # For autoincrement
    birth_loc_df.insert(loc=1, column="TypeOfLocation",
                        value=conn.convertTypeToID(["Geboorteplaats"], "type_of_location")[0])  # Place of birth ID
    birth_loc_df.insert(loc=5, column="EndDate", value=df["geboortedatum"])
    birth_loc_df.insert(loc=6, column="locationPersonID", value=person_df["personPersonID"])
    location_attributes = ["LocationID", "TypeOfLocation", "Country", "City", "locationStartDate", "locationEndDate",
                           "locationPersonID"]
    conn.insert("location", location_attributes, birth_loc_df.replace({np.nan: None}), True)
    # conn.insertMany("location", birth_loc_df.replace({np.nan: None}))

    death_loc_df = df[["Land van overlijden", "Sterfplaats", "Sterfdatum"]]
    # Filter for empty rows in advance
    death_loc_df = death_loc_df[
        death_loc_df["Land van overlijden"].notna() | death_loc_df["Sterfplaats"].notna() | death_loc_df[
            "Sterfdatum"].notna()]
    death_loc_df.insert(loc=0, column="LocationID", value=None)
    death_loc_df.insert(loc=1, column="TypeOfLocation",
                        value=conn.convertTypeToID(["Sterfplaats"], "type_of_location")[0])  # Place of death ID
    death_loc_df.insert(loc=5, column="EndDate", value=df["geboortedatum"])
    death_loc_df.insert(loc=6, column="locationPersonID", value=person_df["personPersonID"])
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
                         value=conn.convertTypeToID(["University Employment"], "type_of_profession")[0])
        period_df.insert(loc=2, column="TypeOfPosition",
                         value=conn.convertTypeToID(df['Aanstelling ' + period], 'type_of_position'))
        period_df.insert(loc=3, column="TypeOfExpertise",
                         value=conn.convertTypeToID(df['Vakgebied ' + period], 'type_of_expertise'))
        period_df.insert(loc=4, column="TypeOfFaculty",
                         value=conn.convertTypeToID(df['Faculteit ' + period], 'type_of_faculty'))
        period_df.insert(loc=7, column="professionPersonID", value=person_df["personPersonID"])

        # Filter entries to exclude empty professions
        period_df = period_df[
            (period_df['Datum aanstelling ' + period].notna()) | (period_df['TypeOfExpertise'].notna()) | (
                period_df['TypeOfPosition'].notna())]
        profession_attributes = ["ProfessionID", "TypeOfProfession", "TypeOfPosition", "TypeOfExpertise",
                                 "TypeOfFaculty", "professionStartDate", "professionEndDate", "professionPersonID"]
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
    person_df = df[
        ["VN standaard", "AN standaard", "AN standaard", "LAND", "RELIGIE INGESCHREVENE", "STATUS INGESCHREVENE"]]
    person_df.insert(loc=0, column="personPersonID", value=range(maxID, maxID + len(person_df)))
    person_df.insert(loc=1, column="TypeOfPerson", value=conn.convertTypeToID(["Student"], "type_of_person")[0])
    person_df.insert(loc=8, column="AVG", value="VRIJ")
    person_attributes = ["personPersonID", "TypeOfPerson", "FirstName", "LastName", "FamilyName", "Nationality",
                         "Religion", "Status", "AVG"]
    conn.insert("person", person_attributes, person_df.replace({np.nan: None}), True)
    # conn.insertMany("person", person_df.replace({np.nan: None}))

    # Create and insert location dataframe
    birth_loc_df = df[["LAND", "VERT PLAATS", "REGIO2 WERELDDEEL"]].replace({np.nan: None})
    birth_loc_df['VERT PLAATS'] = df['VERT PLAATS'].fillna(df['PLAATS as'])  # If 'VERT' is empty, replace with 'as'
    birth_loc_df.insert(loc=0, column="LocationID", value=None)
    birth_loc_df.insert(loc=1, column="TypeOfLocation",
                        value=conn.convertTypeToID(["Geboorteplaats"], "type_of_location")[0])
    birth_loc_df.insert(loc=5, column="Geboortedatum", value=df['GEB JAAR'])
    birth_loc_df.insert(loc=6, column="EndDate", value=birth_loc_df["Geboortedatum"])
    birth_loc_df.insert(loc=7, column="locationPersonID", value=person_df["personPersonID"])
    location_attributes = ["LocationID", "TypeOfLocation", "Country", "City", "Region", "locationStartDate", "locationEndDate",
                           "locationPersonID"]
    conn.insert("location", location_attributes, birth_loc_df.replace({np.nan: None}), True)

    # Create and insert profession dataframe
    profession_attributes = ["ProfessionID", "TypeOfProfession", "TypeOfPosition", "TypeOfFaculty", "professionStartDate",
                             "professionPersonID"]
    # profession_df = pd.DataFrame(columns=["professionPersonID"], data=[person_df["personPersonID"]])
    profession_df = pd.DataFrame()
    profession_df.to_excel("PIDs.xlsx")
    profession_df.insert(loc=0, column="ProfessionID", value=None)
    profession_df.insert(loc=1, column="TypeOfProfession",
                         value=conn.convertTypeToID(["Student"], "type_of_profession")[0])
    profession_df.insert(loc=2, column="TypeOfPosition", value=conn.convertTypeToID(["Student"], "type_of_position")[0])
    profession_df.insert(loc=3, column="TypeOfFaculty",
                         value=conn.convertTypeToID(df['VERT FAC'], "type_of_faculty")[0])
    registrationDate_df = pd.DataFrame(index=range(len(df)), columns=["reg"])
    registrationDate_df["reg"] = df['DATUMJAAR as'].map(str) + '-' + df['DATUMINMND as'].map(str) + '-' + df[
        'DATUMINDAG as'].map(str)
    registrationDate_df["reg"] = registrationDate_df["reg"].apply(checkDate)
    profession_df.insert(loc=4, column="professionStartDate", value=registrationDate_df["reg"])
    profession_df.insert(loc=5, column="professionPersonID", value=person_df["personPersonID"])
    conn.insert("profession", profession_attributes, profession_df.replace({np.nan: None}), True)

    # Commit and close database connection
    del conn


# Hoogleraren - 'Hoogleraren all - Ariadne.xlsx'
def hoogleraren():
    # Handle: http://hdl.handle.net/1887.1/item:[nummer]
    # AVG: Alleen bij waarde "VRIJ" gebruiken
    # Convert excel file to Dataframe
    dateColumns = ["geboortedatum", "Sterfdatum", "Datum", "Datum aanstelling I", "Datum aanstelling II",
                   "Datum aanstelling III", "Datum aanstelling IV", "Einde dienstverband I", "Einde dienstverband II",
                   "Einde dienstverband III", "Einde dienstverband IV"]
    # file_location = r"../data/Hoogleraren all - preprocessed.xlsx"
    file_location = r"../data/Hoogleraren all - Ariadne.xlsx"
    hoogleraren_df = pd.read_excel(file_location, engine='openpyxl', parse_dates=dateColumns).replace({np.nan: None})

    hoogleraren_start = time.time()
    # Correct all dates and remove completely invalid formats
    for column in dateColumns:
        hoogleraren_df[column] = hoogleraren_df[column].apply(checkDate)
    initiateProfessorTypes(hoogleraren_df)
    insertProfessors(hoogleraren_df)
    print(f"\"Professor\" adapter finished successfully in {round(time.time() - hoogleraren_start, 2)} seconds")


# Studenten - 'Alle inschrijvingen 1575-1812.xlsx'
def studenten():
    # Convert excel file to Dataframe
    dateColumns = ['GEB JAAR']
    file_location = r"../data/Alle inschrijvingen 1575-1812.xlsx"
    studenten_df = pd.read_excel(file_location, engine='openpyxl', parse_dates=dateColumns).replace({np.nan: None})

    student_start = time.time()
    # Correct all dates and remove completely invalid formats
    for column in dateColumns:
        studenten_df[column] = studenten_df[column].apply(checkDate)
    initiateStudentTypes(studenten_df)
    insertStudents(studenten_df)
    print(f"\"Student 1575-1812\" adapter finished successfully in {round(time.time() - student_start, 2)} seconds")


# Function only for testing out stuff, can be removed if needed
def playground():
    # dateColumns = ["geboortedatum", "Sterfdatum", "Datum aanstelling I", "Datum aanstelling II",
    #                "Datum aanstelling III", "Datum aanstelling IV", "Einde dienstverband I", "Einde dienstverband II",
    #                "Einde dienstverband III", "Einde dienstverband IV"]
    # # file_location = r"../data/Hoogleraren all - preprocessed.xlsx"
    # file_location = r"../data/Hoogleraren all - Ariadne.xlsx"
    # file_location = r"../data/Alle inschrijvingen 1575-1812.xlsx"
    # df = pd.read_excel(file_location, engine='openpyxl').replace({np.nan: None})

    # # print(len(df[df['Geboorteland'].isin(["Verenigd Koninkrijk"])]))
    # start = time.time()
    # print(f"Program finished successfully in {time.time() - start} seconds")
    # dates = ["1901-1-01", "2000", "1850-02", "Tussen 1635 en 1640", "1996-04-01 ?0", "1621 (voor 9 februari)",
    #          "onbekend", "1971-13-18", "2019-01-00", "1980-13-41", "1957-07-38", "1955-02-29"]
    # new = []
    # for date in dates:
    #     new.append(checkDate(date))
    #     print(date, "\t", checkDate(date))
    # print(new)
    pass


# main
if __name__ == "__main__":
    # start = time.time()
    # playground()
    hoogleraren()  # Check number of incorrect dates
    studenten()

    # print(f"Program finished successfully in {round(time.time() - start, 2)} seconds")
