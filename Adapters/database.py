import mysql.connector
import numpy as np
import pandas as pd


class Connection:
    def __init__(self):
        # Connect to database
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="LinkingUCD",
            password="UCDAdapter",
            database="univercity",
            port="3306"
        )

        self.cursorPrepared = self.mydb.cursor(prepared=True)
        # Main tables
        self.profession = "INSERT INTO profession (ProfessionID, TypeOfProfession, TypeOfPosition, TypeOfExpertise, TypeOfFaculty, StartDate, EndDate, PersonID_engagement) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.location = "INSERT INTO location (LocationID, TypeOfLocation, Country, City, Street, HouseNumber, Region, StartDate, EndDate, PersonID_location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.person = "INSERT INTO person (PersonID, TypeOfPerson, FirstName, LastName, FamilyName, Affix, Nickname, Gender, Nationality, Religion, `Status`, Handles, AVG) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.relation = "INSERT INTO relation (RelationID, TypeOfRelation, FromPersonID, ToPersonID, LinkClass, EventID) VALUES (%s, %s, %s, %s, %s, %s)"
        self.event = "INSERT INTO event (EventID, EventType, EventYear, EventMonth, EventDay, EventPlace, EventRemark) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.source = "INSERT INTO source (SourceID, SourceType, SourceYear, SourceMonth, SourceDay, PermaLink, SourceLastChangeDate, SourceAccessedAt, SourceRemark) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Type tables
        self.type_of_profession = "INSERT INTO type_of_profession (ProfessionID, ProfessionType) VALUES (%s, %s)"
        self.type_of_expertise = "INSERT INTO  type_of_expertise (ExpertiseID, ExpertiseType) VALUES (%s, %s)"
        self.type_of_faculty = "INSERT INTO type_of_faculty (FacultyID, FacultyType) VALUES (%s, %s)"
        self.type_of_location = "INSERT INTO type_of_location (LocationID, LocationType) VALUES (%s, %s)"
        self.type_of_person = "INSERT INTO type_of_person (PersonID, PersonType) VALUES (%s, %s)"
        self.type_of_position = "INSERT INTO type_of_position (PositionID, PositionType) VALUES (%s, %s)"
        self.type_of_relation = "INSERT INTO type_of_relation (RelationID, RelationType) VALUES (%s, %s)"
        self.type_of_source = "INSERT INTO type_of_source (SourceID, SourceType, Rating) VALUES (%s, %s, %s)"

        # Join tables (for many-to-many relations)
        self.person_source = "INSERT INTO person_source (PersonID, SourceID) VALUES (%s, %s)"
        self.profession_source = "INSERT INTO profession_source (ProfessionID, SourceID) VALUES (%s, %s)"
        self.relation_source = "INSERT INTO relation_source (RelationID, SourceID) VALUES (%s, %s)"
        self.location_source = "INSERT INTO location_source (LocationID, SourceID) VALUES (%s, %s)"

        self.sql_insert_dict = {
                                # Main tables
                                "profession": self.profession,
                                "location": self.location,
                                "person": self.person,
                                "relation": self.relation,
                                "event": self.event,
                                "source": self.source,
                                # Type tables
                                "type_of_profession": self.type_of_profession,
                                "type_of_expertise": self.type_of_expertise,
                                "type_of_faculty": self.type_of_faculty,
                                "type_of_location": self.type_of_location,
                                "type_of_person": self.type_of_person,
                                "type_of_position": self.type_of_position,
                                "type_of_relation": self.type_of_relation,
                                "type_of_source": self.type_of_source,
                                # Join tables
                                "person_source": self.person_source,
                                "profession_source": self.profession_source,
                                "relation_source": self.relation_source,
                                "location_source": self.location_source
                                }

    # Destructor terminates connection with database
    def __del__(self):
        self.cursorPrepared.close()
        self.mydb.commit()
        self.mydb.close()
        # print("Connection closed")

    def insertOneByOne(self, table_name, df):
        if not isinstance(df, pd.DataFrame):
            return

        for entry in list(df.itertuples(index=False, name=None)):
            try:
                self.cursorPrepared.execute(self.sql_insert_dict[table_name], entry)
            except mysql.connector.Error as error:
                print("Something went wrong! {}".format(error), table_name)
                print(entry)

    # TODO: accept multiple tables and dfs in one call
    def insertMany(self, table_name, df):
        if not isinstance(df, pd.DataFrame):
            return

        try:
            self.cursorPrepared.executemany(self.sql_insert_dict[table_name],
                                            list(df.itertuples(index=False, name=None)))
        except mysql.connector.Error as error:
            self.mydb.rollback()
            print("Something went wrong! {}".format(error), table_name)

    def selectTypeTable(self, table_name):
        match table_name:
            case "type_of_profession":
                return pd.read_sql_query("SELECT ProfessionID, ProfessionType FROM type_of_profession",
                                         self.mydb).replace({np.nan: None})
            case "type_of_expertise":
                return pd.read_sql_query("SELECT ExpertiseID, ExpertiseType FROM type_of_expertise", self.mydb).replace(
                    {np.nan: None})
            case "type_of_faculty":
                return pd.read_sql_query("SELECT FacultyID, FacultyType FROM type_of_faculty", self.mydb).replace(
                    {np.nan: None})
            case "type_of_location":
                return pd.read_sql_query("SELECT LocationID, LocationType FROM type_of_location", self.mydb).replace(
                    {np.nan: None})
            case "type_of_person":
                return pd.read_sql_query("SELECT PersonID, PersonType FROM type_of_person", self.mydb).replace(
                    {np.nan: None})
            case "type_of_position":
                return pd.read_sql_query("SELECT PositionID, PositionType FROM type_of_position", self.mydb).replace(
                    {np.nan: None})
            case "type_of_relation":
                return pd.read_sql_query("SELECT RelationID, RelationType FROM type_of_relation", self.mydb).replace(
                    {np.nan: None})
            case "type_of_source":
                return pd.read_sql_query("SELECT SourceID, SourceType, Rating FROM type_of_source", self.mydb).replace(
                    {np.nan: None})
            case _:
                print("Invalid type table!")
                return None

    # TODO: find "gaps" in available IDs (as a result of deletion) to reuse
    def getPersonMaxID(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT max(PersonID) FROM person")
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    # def getRelationMaxID(self):
    #     return

    # Deprecated
    # def getProfessors(self):
    #     cursor = self.mydb.cursor()
    #     cursor.execute("SELECT * FROM person WHERE TypeOfPerson = 1")
    #     result = cursor.fetchall()
    #     cursor.close()
    #     return result

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

    # Extract multiple tables and change dash for integration
    def getIndividualInfo(self, type_of_person):
        cursor = self.mydb.cursor()
        results = []

        if type_of_person == 0:  # Select all types of persons
            query = """SELECT PersonID, FirstName, LastName, Gender, Nationality FROM person"""
            cursor.execute(query)
        else:
            query = """SELECT PersonID, FirstName, LastName, Gender, Nationality FROM person WHERE TypeOfPerson = %s"""
            cursor.execute(query % type_of_person)
        result_df = pd.DataFrame(cursor.fetchall(), columns=["PersonID", "FN", "LN", "Gender", "Nationality"])
        """ TODO:
                Birth/death info -> location table
                Profession info -> profession table
                Rating -> source table
        """
        cursor.close()
        return result_df

    def checkTableName(self, table_name):
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

    def selectProfessor(self, table_name, attributes):
        if not self.checkTableName(table_name):
            print("selectProfessor:", table_name, "is invalid!")
            return pd.DataFrame()

        cursor = self.mydb.cursor()
        # type_of_person = 1  # Professor
        format_strings = ', '.join(['%s'] * len(attributes))
        query = "SELECT %s FROM {tn} WHERE {tn}.TypeOfPerson = 1 AND {tn}.AVG='VRIJ'".format(tn=table_name)
        cursor.execute(query % format_strings % tuple(attributes))
        result_df = pd.DataFrame(cursor.fetchall(), columns=attributes)
        cursor.close()
        return result_df


# Main
if __name__ == "__main__":
    conn = Connection()
    prof_person_df = conn.selectProfessor("person", ["PersonID", "FirstName", "LastName", "Gender"])
    prof_person_df.rename(columns=dict(zip(["FirstName", "LastName"], ["First name", "Last name"])), inplace=True)
    print(prof_person_df)
    # conn.checkTableName("persons")
    del conn
    # print("database.py")
