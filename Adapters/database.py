import mysql.connector
import numpy as np
import pandas as pd
from tenacity import retry, wait_exponential, stop_after_attempt


class Connection:
    @retry(wait=wait_exponential(multiplier=2, min=1, max=10), stop=stop_after_attempt(5))
    def __init__(self):
        # Connect to database
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user="LinkingUCD",
                password="UCDAdapter",
                database="univercity",
                port="3306"
            )
            # print("Connection to database successful")
        except Exception:
            print("Connection to database failed, retrying.")
            raise Exception

    # Destructor terminates connection with database
    def __del__(self):
        # self.cursorPrepared.close()
        self.mydb.commit()
        self.mydb.close()
        # print("Connection closed")

    # def insertOneByOne(self, table_name, df):
    #     if not isinstance(df, pd.DataFrame):
    #         return
    #
    #     for entry in list(df.itertuples(index=False, name=None)):
    #         try:
    #             self.cursorPrepared.execute(self.sql_insert_dict[table_name], entry)
    #         except mysql.connector.Error as error:
    #             print("Something went wrong! {}".format(error), table_name)
    #             print(entry)

    # def insertMany(self, table_name, df):
    #     if not isinstance(df, pd.DataFrame):
    #         return
    #
    #     try:
    #         self.cursorPrepared.executemany(self.sql_insert_dict[table_name],
    #                                         list(df.itertuples(index=False, name=None)))
    #     except mysql.connector.Error as error:
    #         self.mydb.rollback()
    #         print("Something went wrong! {}".format(error), table_name)

    def selectTypeTable(self, table_name):
        if table_name == "type_of_profession":
            return pd.read_sql_query("SELECT ProfessionID, ProfessionType FROM type_of_profession",
                                     self.mydb).replace({np.nan: None})
        elif table_name == "type_of_expertise":
            return pd.read_sql_query("SELECT ExpertiseID, ExpertiseType FROM type_of_expertise", self.mydb).replace(
                {np.nan: None})
        elif table_name == "type_of_faculty":
            return pd.read_sql_query("SELECT FacultyID, FacultyType FROM type_of_faculty", self.mydb).replace(
                {np.nan: None})
        elif table_name ==  "type_of_location":
            return pd.read_sql_query("SELECT LocationID, LocationType FROM type_of_location", self.mydb).replace(
                {np.nan: None})
        elif table_name ==  "type_of_person":
            return pd.read_sql_query("SELECT PersonID, PersonType FROM type_of_person", self.mydb).replace(
                {np.nan: None})
        elif table_name ==  "type_of_position":
            return pd.read_sql_query("SELECT PositionID, PositionType FROM type_of_position", self.mydb).replace(
                {np.nan: None})
        elif table_name ==  "type_of_relation":
            return pd.read_sql_query("SELECT RelationID, RelationType FROM type_of_relation", self.mydb).replace(
                {np.nan: None})
        elif table_name ==  "type_of_source":
            return pd.read_sql_query("SELECT SourceID, SourceType, Rating FROM type_of_source", self.mydb).replace(
                {np.nan: None})
        else:
            print("Invalid type table!")
            return None

    # TODO: find "gaps" in available IDs (as a result of deletion) to reuse
    def getPersonMaxID(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT max(PersonID) FROM person")
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    def getProfIDs(self):
        """
        :return: List containing PersonIDs of all professors
        """
        cursor = self.mydb.cursor()
        cursor.execute("SELECT PersonID FROM person WHERE TypeOfPerson = 1")
        result = cursor.fetchall()
        cursor.close()
        return result

    # TODO: add relations and profession (and source)
    def getProfInfo(self, prof_id):
        """
        Function for fetching info from person/professor for linking
        :param prof_id: PersonID of professors
        :return: List of tuples with person and location info
        """
        cursor = self.mydb.cursor()
        result = []
        queryPerson = """SELECT FirstName, Affix, LastName, Gender, Nationality FROM person WHERE PersonID = %s"""
        cursor.execute(queryPerson % prof_id)
        result.append({"person": cursor.fetchall()})
        queryLocation = """SELECT Country, City, Street, StartDate, TypeOfLocation FROM location WHERE PersonID_location = %s"""
        cursor.execute(queryLocation % prof_id)
        result.append({"locations": cursor.fetchall()})
        cursor.close()
        return result

    def checkTableName(self, table_name):
        """
        Check if given table name is valid
        :param table_name: name of database table
        :return: True when table name exists, else False
        """
        cursor = self.mydb.cursor()
        query = "SELECT table_name FROM information_schema.tables WHERE TABLE_SCHEMA = 'univercity'"
        # query = "SHOW tables"
        cursor.execute(query)
        table_names = cursor.fetchall()
        table_names = [i[0] for i in table_names]
        if table_name in table_names:
            return True
        else:
            return False

    def selectProfessor(self, table_name, attributes, where_clause):
        """
        Select data for professors using dynamic queries
        :param table_name: name of table to be selected
        :param attributes: list of attributes
        :param where_clause: where clause
        :return: DataFrame with query result
        """
        if not self.checkTableName(table_name):
            print("selectProfessor:", table_name, "is invalid!")
            return pd.DataFrame()

        cursor = self.mydb.cursor()
        format_strings = ', '.join(['%s'] * len(attributes)) % tuple(attributes)
        query = ("SELECT %s FROM {tn} %s" % (format_strings, where_clause))
        query = query.format(tn=table_name).strip()
        # print(query)
        cursor.execute(query)

        # Fetch all column names when asterix is used
        if "*" in attributes:
            attributes = [i[0] for i in cursor.description]

        # .set_index Only works when ID is at the first position in [attributes]
        result_df = pd.DataFrame(cursor.fetchall(), columns=attributes).set_index(attributes[0])
        cursor.close()
        return result_df

    def insert(self, table_name, attributes, values_df, prepared=True):
        if not self.checkTableName(table_name):
            print("insert:", table_name, "is invalid!")
            return
        if values_df is None:
            return
        if prepared:
            # Optimization for execution of many equal or similar consecutive queries
            cursor = self.mydb.cursor(prepared=True)
        else:
            # Currently unused -> use for record linker
            cursor = self.mydb.cursor(prepared=False)

        format_strings = ', '.join(['%s'] * len(attributes))
        query = ("INSERT INTO {tn} (%s) VALUES (%s)" % (format_strings % tuple(attributes), format_strings))
        query = query.format(tn=table_name).strip()
        # print(query)
        try:
            cursor.executemany(query, list(values_df.itertuples(index=False, name=None)))
        except mysql.connector.Error as error:
            self.mydb.rollback()
            print("Something went wrong when inserting! {}".format(error), table_name)
        cursor.close()
        self.mydb.commit()


# Main
if __name__ == "__main__":
    # conn = Connection()
    # del conn
    print("database.py")
