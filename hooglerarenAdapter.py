import database
import numpy as np
import pandas as pd
import datetime
import time
from operator import itemgetter
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)


# Fix dates that do not match the format and add to new df column
# If save_raw is True, raw value of "wrong" date will be saved in a new column
# Note: some not easily fixable dates (i.e. "1885-03-27, met ingang 1885-04-01") are ignored and discarded
def fixDates(df, columns, save_raw):
    if save_raw:
        for column in columns:
            new_dates = []
            for Dod in df[column]:
                if Dod is None:
                    new_dates.append(None)
                    continue
                # Dod = "".join(c for c in Dod if c.isdecimal() or c is '-')
                if len(Dod) == 4 and Dod.isdigit():
                    new_dates.append(Dod + "-01-01")
                    continue
                elif len(Dod) == 7 and Dod[0:4].isdigit() and Dod[5:].isdigit():
                    try:
                        datetime.datetime.strptime(Dod, "%Y-%m")
                        new_dates.append(Dod + "-01")
                    except ValueError:
                        new_dates.append(None)
                    continue
                try:
                    datetime.datetime.strptime(Dod, "%Y-%m-%d")
                    new_dates.append(Dod)
                except ValueError:
                    new_dates.append(None)
            df[column + "_checked"] = new_dates
    else:
        for column in columns:
            for Dod in df[column]:
                if Dod is None:
                    continue
                # Dod = "".join(c for c in Dod if c.isdecimal() or c is '-')
                if len(Dod) == 4 and Dod.isdigit():
                    df = df.replace(Dod, Dod + "-01-01")
                    continue
                elif len(Dod) == 7 and Dod[0:4].isdigit() and Dod[5:].isdigit():
                    try:
                        datetime.datetime.strptime(Dod, "%Y-%m")
                        df = df.replace(Dod, Dod + "-01")
                    except ValueError:
                        df = df.replace(Dod, None)
                    continue
                try:
                    datetime.datetime.strptime(Dod, "%Y-%m-%d")
                except ValueError:
                    df = df.replace(Dod, None)
                    # print(column, Dod)
    return df


# Initiate typed tables
def initiateTypes(df):
    engagement = [[None, "Employment"], [None, "Guest"], [None, "Student"]]
    expertise = getTypesPerColumn(df[["Vakgebied I", "Vakgebied II", "Vakgebied III", "Vakgebied IV"]])
    faculty = getTypesPerColumn(df[["Faculteit I", "Faculteit II", "Faculteit III", "Faculteit IV"]])
    location = [[None, "Geboorteplaats"], [None, "Sterfplaats"]]
    person = [[None, "Professor"], [None, "Student"]]
    position = getTypesPerColumn(df[["Aanstelling I", "Aanstelling II", "Aanstelling III", "Aanstelling IV"]])

    # Connect with database
    conn = database.Connection()
    conn.insertMany("type_of_engagement", pd.DataFrame(engagement))
    conn.insertMany("type_of_expertise", pd.DataFrame(expertise))
    conn.insertMany("type_of_faculty", pd.DataFrame(faculty))
    conn.insertMany("type_of_location", pd.DataFrame(location))
    conn.insertMany("type_of_person", pd.DataFrame(person))
    conn.insertMany("type_of_position", pd.DataFrame(position))

    # Commit and close database connection
    del conn


# Return sorted list of unique types per column
def getTypesPerColumn(type_df):
    type_list = []
    for column in type_df:
        for row in type_df[column]:
            if not any(row in sublist for sublist in type_list):
                type_list.append([None, row])
    return sorted(type_list, key=itemgetter(1))


# Converts textual type to TypeID
def convertTypeToID(conn, df_column, table_name):
    IDs = []
    type_df = conn.selectTypeTable(table_name)
    for old_type in df_column:
        if old_type is None:
            IDs.append(None)
            continue
        for typeID, typeText in type_df.itertuples(index=False):
            if old_type == typeText:
                IDs.append(int(typeID))
    return IDs


# Process and insert professor data
def insert(df):
    # Connect with database
    conn = database.Connection()

    """
    Create and insert person dataframe
    """
    maxID = conn.getPersonMaxID()
    if maxID is None:
        maxID = 0
    maxID += 1
    person_df = df[["Voornamen", "Achternaam", "Roepnaam", "Geslacht", "Geboorteland"]]
    person_df.insert(loc=0, column="PersonID", value=range(maxID, len(person_df) + 1))
    person_df.insert(loc=3, column="Affix", value=None)
    person_df.insert(loc=7, column="TypeOfPerson", value=1)  # Professor ID
    conn.insertMany("person", person_df.replace({np.nan: None}))

    """
    Create and insert location dataframe
    Two types of locations: birth(1) and death(2)
    """
    birth_location_df = df[["Geboorteland", "Geboorteplaats", "geboortedatum"]]
    birth_location_df.insert(loc=0, column="LocationID", value=None)
    birth_location_df.insert(loc=1, column="TypeOfLocation", value=1)  # PLace of birth ID
    birth_location_df.insert(loc=4, column="Region", value=None)
    birth_location_df.insert(loc=6, column="EndDate", value=df["geboortedatum"])
    birth_location_df.insert(loc=7, column="PersonID", value=person_df["PersonID"])
    conn.insertMany("location", birth_location_df.replace({np.nan: None}))

    death_location_df = df[["Land van overlijden", "Sterfplaats", "Sterfdatum"]]
    death_location_df.insert(loc=0, column="LocationID", value=None)
    death_location_df.insert(loc=1, column="TypeOfLocation", value=2)  # Place of death ID
    death_location_df.insert(loc=4, column="Region", value=None)
    death_location_df.insert(loc=6, column="EndDate", value=df["Sterfdatum"])
    death_location_df.insert(loc=7, column="PersonID", value=person_df["PersonID"])
    conn.insertMany("location", death_location_df.replace({np.nan: None}))

    """
    Create and insert engagement dataframe
    """
    periods = ['I', 'II', 'III', 'IV']
    for period in periods:
        period_df = df[['Datum aanstelling ' + period, 'Einde dienstverband ' + period]].replace({np.nan: None})
        period_df.insert(loc=0, column="EngagementID", value=None)
        period_df.insert(loc=1, column="TypeOfPosition", value=convertTypeToID(conn, df['Aanstelling ' + period], 'type_of_position'))
        period_df.insert(loc=2, column="TypeOfExpertise", value=convertTypeToID(conn, df['Vakgebied ' + period], 'type_of_expertise'))
        period_df.insert(loc=5, column="TypeOfFaculty", value=convertTypeToID(conn, df['Faculteit ' + period], 'type_of_faculty'))
        period_df.insert(loc=6, column="TypeOfEngagement", value=1)  # Employment ID
        period_df.insert(loc=7, column="PersonID", value=person_df["PersonID"])
        # Filter entries to exclude empty engagements
        period_df = period_df[(period_df['Datum aanstelling ' + period].notna()) | (period_df['TypeOfExpertise'].notna()) | (period_df['TypeOfPosition'].notna())]
        conn.insertMany("engagement", period_df.replace({np.nan: None}))

    # Commit and close database connection
    del conn


if __name__ == "__main__":
    # start = time.time()
    # Convert excel file to Dataframe
    file_location = r"data/Hoogleraren all.xlsx"
    hoogleraren_df = pd.read_excel(file_location, engine='openpyxl').replace({np.nan: None})

    # Fix dates
    dateColumns = ["geboortedatum", "Sterfdatum", "Datum aanstelling I", "Datum aanstelling II",
                   "Datum aanstelling III", "Datum aanstelling IV", "Einde dienstverband I", "Einde dienstverband II",
                   "Einde dienstverband III", "Einde dienstverband IV"]
    hoogleraren_df = fixDates(hoogleraren_df, dateColumns, False)

    initiateTypes(hoogleraren_df)
    insert(hoogleraren_df)
    # print(f"Time: {time.time() - start} seconds")
