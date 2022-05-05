import datetime
import mysql.connector
import pandas as pd
import numpy as np
from collections import defaultdict
from sqlalchemy import create_engine

# Connect to database
mydb = mysql.connector.connect(
    host="localhost",
    user="LinkingUCD",
    password="UCDAdapter",
    database="test_via_eer",
    port="3306"
)


# Return True if table exists, else false
def checkIfTableExists(table_to_check):
    cursor = mydb.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'test_via_eer'")
    tables = cursor.fetchall()

    for table in tables:
        if table_to_check == str(table)[2:str(table).find('\',')]:
            cursor.close()
            return True
    print("Table does not exist")
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
def insert(table_name, val):
    i_cursor = mydb.cursor()
    # Check if entry already exists, else UPDATE?
    sql = """INSERT INTO %s (idPerson, Firstname, Lastname, Pob, Pod, Gender, Dob, Dod) VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s)"""
    i_cursor.executemany(sql % table_name, val)
    i_cursor.close()


# Delete all contents of table without removing table
def deleteTableAll(table_name):
    if checkIfTableExists(table_name):
        d_cursor = mydb.cursor()
        sql = """DELETE FROM %s"""
        d_cursor.execute(sql % table_name)
        d_cursor.close()


# Remove dates that do not match the format
def fixDates(df, name):
    for column in name.split(', '):
        for Dod in df[column]:
            if Dod is None:
                continue
            try:
                datetime.datetime.strptime(Dod, "%Y-%m-%d")
            except ValueError:
                df = df.replace(Dod, None)
    return df


# main
if __name__ == '__main__':
    # using openpyxl for .xlsx files
    excel_full = pd.read_excel(r"Hoogleraren all.xlsx", engine='openpyxl')

    # To add: call sign and isEnrolled
    df_person = pd.DataFrame(excel_full,
                             columns=["ID", "Voornamen", "Achternaam", "Geboorteplaats", "Sterfplaats", "Geslacht",
                                      "geboortedatum", "Sterfdatum"])
    df_person = df_person.replace({np.nan: None})
    df_person = fixDates(df_person, "Sterfdatum, geboortedatum")

    # deleteTableAll("person")
    # select("person")
    insert("person", list(df_person.itertuples(index=False, name=None)))
    select("person")

    mydb.commit()
    mydb.close()
