import mysql.connector
import numpy as np
import pandas as pd
from tenacity import retry, wait_exponential, stop_after_attempt
import time
import sqlalchemy


# class Query:
#     def __init__(self, connection):
#         self.connection = connection
#
#     def __del__(self):
#         pass
#
#     def select(self, table_name, attributes=None, values_df=None, prepared=True):
#         if not self.checkTableName(table_name):
#             print("insert:", table_name, "is invalid!")
#             return
#         if values_df is None:
#             return
#         if prepared:
#             # Optimization for consecutive execution of many equal or similar queries
#             cursor = self.mydb.cursor(prepared=True)
#         else:
#             # Currently unused -> use for instance for record linker when inserting a small number
#             cursor = self.mydb.cursor(prepared=False)
#
#         format_strings = ', '.join(['%s'] * len(attributes))
#         query = ("INSERT INTO {tn} (%s) VALUES (%s)" % (format_strings % tuple(attributes), format_strings))
#         query = query.format(tn=table_name).strip()
#         # print(query)
#         try:
#             cursor.executemany(query, list(values_df.itertuples(index=False, name=None)))
#         except mysql.connector.Error as error:
#             self.mydb.rollback()
#             print("Something went wrong when inserting! {}".format(error), table_name)
#         cursor.close()
#         self.mydb.commit()
#
#     def join(self):
#         pass


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
        elif table_name == "type_of_location":
            return pd.read_sql_query("SELECT LocationID, LocationType FROM type_of_location", self.mydb).replace(
                {np.nan: None})
        elif table_name == "type_of_person":
            return pd.read_sql_query("SELECT PersonID, PersonType FROM type_of_person", self.mydb).replace(
                {np.nan: None})
        elif table_name == "type_of_position":
            return pd.read_sql_query("SELECT PositionID, PositionType FROM type_of_position", self.mydb).replace(
                {np.nan: None})
        elif table_name == "type_of_relation":
            return pd.read_sql_query("SELECT RelationID, RelationType FROM type_of_relation", self.mydb).replace(
                {np.nan: None})
        elif table_name == "type_of_source":
            return pd.read_sql_query("SELECT SourceID, SourceType, Rating FROM type_of_source", self.mydb).replace(
                {np.nan: None})
        else:
            print("Invalid type table!")
            return None

    # TODO: find "gaps" in available IDs (as a result of deletion) to reuse
    def getPersonMaxID(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT max(personPersonID) FROM person")
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    def getProfIDs(self):
        """
        :return: List containing PersonIDs of all professors
        """
        cursor = self.mydb.cursor()
        cursor.execute("SELECT personPersonID FROM person WHERE TypeOfPerson = 1")
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
        queryPerson = """SELECT FirstName, Affix, LastName, Gender, Nationality FROM person WHERE personPersonID = %s"""
        cursor.execute(queryPerson % prof_id)
        result.append({"person": cursor.fetchall()})
        queryLocation = """SELECT Country, City, Street, locationStartDate, TypeOfLocation FROM location WHERE locationPersonID = %s"""
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

    def getAttributeNames(self, table: str) -> list:
        if not self.checkTableName(table):
            print("Incorrect table name when executing \"getAttributeNames\"")
            return []
        cursor = self.mydb.cursor()
        cursor.execute("SHOW columns FROM " + table)
        res = cursor.fetchall()
        attributeNames = [i[0] for i in res]
        cursor.close()
        return attributeNames

    def findTableName(self, attribute: str) -> str:
        query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME LIKE '%{}%' " \
                "AND TABLE_SCHEMA='Univercity'".format(attribute)
        cursor = self.mydb.cursor()
        cursor.execute(query)
        table_name = cursor.fetchone()
        cursor.close()
        if table_name is not None:
            return table_name[0]
        else:
            print("Cannot find table corresponding to attribute:", attribute)
            return ""

    # Converts textual type to TypeID
    def convertTypeToID(self, textual_types, table_name):
        """
        Converts list/pd series of "textual" types to corresponding IDs
        :param textual_types: list or pd series containing textual types
        :param table_name: name of type table to retrieve IDs from
        :return: list IDs in the same order as the input
        """
        IDs = []
        type_df = self.selectTypeTable(table_name)
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

    def QueryBuilderPublic(self, attributes: list, tables: list, main_col_name: str, person_type: str, where: list) -> pd.DataFrame:
        year = "SUBSTRING({table}StartDate, 1, 4)".format(table=tables[0])
        century = "SUBSTRING({table}StartDate, 1, 2) + 1".format(table=tables[0])
        person_type = self.convertTypeToID([person_type], "type_of_person")[0]

        if attributes[0] == 'StartDate':
            attributes[0] = year
        elif attributes[0] == 'EndDate':
            year = year.replace('StartDate', 'EndDate')
            century = century.replace('StartDate', 'EndDate')
            attributes[0] = year

        if not where:  # if "where" is empty convert to empty string
            where = ""
        else:  # if "where" is NOT empty convert to correct syntax
            where = " AND " + " AND ".join(where)

        # Add join to translate from type "number" to textual description
        type_join = ""
        if len(tables) == 2:
            type_name = tables[1].split('_')[-1].capitalize()
            type_id = self.getAttributeNames(tables[1])[0]
            type_join = f" JOIN {tables[1]} ON {type_id} = TypeOf{type_name}"

        query = "SELECT {attr} as '{attrName}', count({attr}) as 'count', {year} as 'year', {century} as 'century'" \
                " FROM {table}" \
                " JOIN person ON personPersonID = {table}PersonID AND TypeOfPerson = {person_type}{type_join}" \
                " WHERE {table}StartDate IS NOT NULL AND {attr} IS NOT NULL{where}" \
                " GROUP BY {year}, {attr}" \
                " ORDER BY {year} ASC".format(attr=attributes[0], attrName=main_col_name, year=year, century=century,
                                              table=tables[0], where=where, person_type=person_type, type_join=type_join)

        if 'EndDate' in attributes[0]:
            query = query.replace('StartDate', 'EndDate')
        cursor = self.mydb.cursor()
        cursor.execute(query)
        attributes = [i[0] for i in cursor.description]
        result_df = pd.DataFrame(cursor.fetchall(), columns=attributes)
        result_df = result_df.astype({main_col_name: 'string', 'count': 'int64', 'year': 'int64', 'century': 'int64'})
        cursor.close()
        return result_df

    def QueryBuilderPivotTable(self, index, values, columns, aggfunc):
        attributes = index + values + columns
        query = "SELECT " + ', '.join(attributes)
        tables = []
        # Get tables to which attributes belong
        for attr in attributes:
            table_name = self.findTableName(attr)
            if table_name != "" and table_name not in tables:
                tables.append(table_name)

        print(tables)
        query += " FROM " + tables[0]
        # Add joins for each table
        for table in tables[1:]:
            query += " JOIN {table} ON {table}PersonID = {table2}PersonID".format(table=table, table2=tables[0])
        print(query)
        # query += " WHERE Gender IS NOT NULL"
        cursor = self.mydb.cursor()
        cursor.execute(query)
        result_df = pd.DataFrame(cursor.fetchall(), columns=attributes)
        cursor.close()
        return result_df, pd.pivot_table(result_df, index=index, columns=columns, values=values, aggfunc=aggfunc)

    def select(self, table_name, attributes, where_clause):
        """
        Select data from database using dynamic queries
        :param table_name: name of table to be selected
        :param attributes: list of attributes
        :param where_clause: where clause
        :return: DataFrame with query result
        """
        if not self.checkTableName(table_name):
            print("select:", table_name, "is invalid!")
            return pd.DataFrame()

        cursor = self.mydb.cursor()
        format_strings = ', '.join(['%s'] * len(attributes)) % tuple(attributes)
        query = ("SELECT %s FROM {tn} %s" % (format_strings, where_clause))
        query = query.format(tn=table_name).strip()
        print(query)
        cursor.execute(query)

        # Fetch all column names when asterix is used
        if "*" in attributes:
            attributes = [i[0] for i in cursor.description]

        # .set_index Only works when ID is at the first position in [attributes]
        result_df = pd.DataFrame(cursor.fetchall(), columns=attributes).convert_dtypes().set_index(attributes[0])
        cursor.close()
        return result_df

    def insert(self, table_name, attributes=None, values_df=None, prepared=True):
        if not self.checkTableName(table_name):
            print("insert:", table_name, "is invalid!")
            return
        if values_df is None:
            return
        if prepared:
            # Optimization for consecutive execution of many equal or similar queries
            cursor = self.mydb.cursor(prepared=True)
        else:
            # Currently unused -> use for instance for record linker when inserting a small number
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
    conn = Connection()
    start = time.time()
    res = conn.QueryBuilderPublic(['Region'], ['location'], "region", "student", ["TypeOfLocation = 1"])
    print(res)
    del conn
    # print(result_df.replace({np.nan: None}).head(45).to_string())
    print(f"Program finished successfully in {time.time() - start} seconds")
