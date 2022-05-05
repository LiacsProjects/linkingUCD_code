import datetime
import mysql.connector
import pandas as pd
import numpy as np
from collections import defaultdict
from sqlalchemy import create_engine


def checkIfTableExists(cursor, table_to_check):
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'test_via_eer'")
    tables = cursor.fetchall()

    for table in tables:
        if table_to_check == str(table)[2:str(table).find('\',')]:
            return True
    print("Table does not exist")
    return False


def select(s_cursor):
    s_cursor.execute("SELECT * FROM person")
    result = s_cursor.fetchall()
    print("SELECT:")
    for person in result:
        print(person)


def insert(i_cursor, table_name, val):
    # Check if entry already exists, else UPDATE?
    sql = """INSERT INTO %s (idPerson, Firstname, Lastname, Pob, Pod, Gender, Dob, Dod) VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s)"""
    i_cursor.executemany(sql % table_name, val)


def deleteTableAll(d_cursor, table_name):
    # Add check if table exists
    if checkIfTableExists(d_cursor, table_name):
        sql = """DELETE FROM %s"""
        d_cursor.execute(sql % table_name)


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


if __name__ == '__main__':
    # using openpyxl for .xlsx files
    excel_full = pd.read_excel(r"Hoogleraren all.xlsx", engine='openpyxl')

    # To add: call sign and isEnrolled
    df_person = pd.DataFrame(excel_full,
                             columns=["ID", "Voornamen", "Achternaam", "Geboorteplaats", "Sterfplaats", "Geslacht",
                                      "geboortedatum", "Sterfdatum"])
    df_person = df_person.replace({np.nan: None})
    df_person = fixDates(df_person, "Sterfdatum, geboortedatum")

    mydb = mysql.connector.connect(
        host="localhost",
        user="LinkingUCD",
        password="UCDAdapter",
        database="test_via_eer",
        port="3306"
    )

    mycursor = mydb.cursor()
    select(mycursor)

    deleteTableAll(mycursor, "person")
    insert(mycursor, "person", list(df_person.itertuples(index=False, name=None)))

    select(mycursor)

    # deleteTableAll(mycursor, "person")

    # select(mycursor)

    mydb.commit()
    mydb.close()
