import datetime
import mysql.connector
import pandas as pd
import numpy as np

# Connect to database
mydb = mysql.connector.connect(
    host="localhost",
    user="LinkingUCD",
    password="UCDAdapter",
    database="test_via_eer",
    port="3306"
)


# Return True if table exists, else False
def checkIfTableExists(table_to_check):
    cursor = mydb.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'test_via_eer'")
    tables = cursor.fetchall()

    for table in tables:
        if table_to_check == str(table)[2:str(table).find('\',')]:
            cursor.close()
            return True
    cursor.close()
    return False


def select(table_name):
    s_cursor = mydb.cursor()
    s_cursor.execute("""SELECT * FROM %s""" % table_name)
    result = s_cursor.fetchall()
    print("SELECT:")
    for person in result:
        print(person)
    s_cursor.close()


# val is data from excel file
# Check if entry already exists, else UPDATE?
def insert(df, table_name):
    if not checkIfTableExists(table_name):
        print("INSERT: Table does not exist")
        return

    i_cursor = mydb.cursor()
    dates = []
    if table_name is "person":
        sql = """INSERT INTO %s (idPerson, Firstname, Lastname, `Call sign`, Pob, Pod, Gender, isEnrolled, Dob, Dod) VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s)"""
        df = pd.DataFrame(df, columns=["ID", "Voornamen", "Achternaam", None, "Geboorteplaats", "Sterfplaats",
                                       "Geslacht", None, "geboortedatum", "Sterfdatum"])
        dates.extend(["geboortedatum", "Sterfdatum"])
    elif table_name is "professor":
        # How to handle multiple disciplines? What are the IDs?
        sql = """INSERT INTO %s (ProfessorID, Nobelaward, Appointment, Discipline, Doa, Employee_EmployeeID, Employee_Person_idPerson) VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s)"""
        df = pd.DataFrame(df, columns=["ID", "Nobelprijs", "Aanstelling I", "Vakgebied I", "Datum aanstelling I",
                                       "ID", "ID"])
        dates.append("Datum aanstelling I")
    else:
        return

    # Replace empty values with None (null in MySQL)
    df = df.replace({np.nan: None})
    # Filter dates, how to handle without losing data? Maybe alter data before?
    df = fixDates(df, dates)

    try:
        i_cursor.executemany(sql % table_name, list(df.itertuples(index=False, name=None)))
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Something went wrong! {}".format(error))
    i_cursor.close()


# Delete all contents of table without removing table
def deleteTableAll(table_name):
    if checkIfTableExists(table_name):
        d_cursor = mydb.cursor()
        sql = """DELETE FROM %s"""
        d_cursor.execute(sql % table_name)
        d_cursor.close()


# Remove dates that do not match the format
def fixDates(df, columns):
    for column in columns:
        for Dod in df[column]:
            if Dod is None:
                continue
            # Dod = "".join(c for c in Dod if c.isdecimal() or c is '-')
            if len(Dod) is 4 and Dod.isdigit():
                df = df.replace(Dod, Dod + "-01-01")
                continue
            try:
                datetime.datetime.strptime(Dod, "%Y-%m-%d")
            except ValueError:
                print(Dod)
                df = df.replace(Dod, None)
    return df


# TODO: Prepare data/file before extracting
def preprocess():
    return


# main
if __name__ == '__main__':
    # Using openpyxl for .xlsx files
    excel_hoogleraren_df = pd.read_excel(r"data/Hoogleraren all.xlsx", engine='openpyxl')

    deleteTableAll("person")
    # Insert data from excel per table
    insert(excel_hoogleraren_df, "person")
    # insert(excel_hoogleraren_df, "professor")

    # deleteTableAll("person")
    # select("person")

    # Commit to save changes to database and close
    mydb.commit()
    mydb.close()
