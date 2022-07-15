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
            database="lucd_reduced",
            port="3306"
        )
        print("Connection opened")

        self.engagement = "INSERT INTO engagement (EngagementID, TypeOfPosition, TypeOfExpertise, StartDate, EndDate, TypeOfFaculty, TypeOfEngagement, PersonID_engagement) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.location = "INSERT INTO location (LocationID, TypeOfLocation, Country, City, Region, StartDate, EndDate, PersonID_location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.person = "INSERT INTO person (PersonID, FirstName, LastName, Affix, Nickname, Gender, Nationality, TypeOfPerson_fk) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.person_to_person = "INSERT INTO person_to_person (PersonToPersonID, FromPersonID, ToPersonID, TypeOfRelation) VALUES (%s, %s, %s, %s)"
        self.type_of_engagement = "INSERT INTO type_of_engagement (EngagementID, EngagementType) VALUES (%s, %s)"
        self.type_of_expertise = "INSERT INTO  type_of_expertise (ExpertiseID, ExpertiseType) VALUES (%s, %s)"
        self.type_of_faculty = "INSERT INTO type_of_faculty (FacultyID, FacultyType) VALUES (%s, %s)"
        self.type_of_location = "INSERT INTO type_of_location (LocationID, LocationType) VALUES (%s, %s)"
        self.type_of_person = "INSERT INTO type_of_person (PersonID, PersonType) VALUES (%s, %s)"
        self.type_of_position = "INSERT INTO type_of_position (PositionID, PositionType) VALUES (%s, %s)"
        self.type_of_relation = "INSERT INTO type_of_relation (RelationID, RelationType) VALUES (%s, %s)"
        self.sql_insert_dict = {"engagement": self.engagement,
                                "location": self.location,
                                "person": self.person,
                                "person_to_person": self.person_to_person,
                                "type_of_engagement": self.type_of_engagement,
                                "type_of_expertise": self.type_of_expertise,
                                "type_of_faculty": self.type_of_faculty,
                                "type_of_location": self.type_of_location,
                                "type_of_person": self.type_of_person,
                                "type_of_position": self.type_of_position,
                                "type_of_relation": self.type_of_relation
                                }

    # Destructor terminates connection with database
    def __del__(self):
        self.mydb.commit()
        self.mydb.close()
        print("Connection closed")

    def insertOneByOne(self, table_name, df):
        # TODO: Test speed difference with/out prepared=True
        cursor = self.mydb.cursor(prepared=True)
        # self.df = pd.DataFrame(self.df, columns=columns)

        for entry in list(df.itertuples(index=False, name=None)):
            try:
                cursor.execute(self.sql_insert_dict[table_name], entry)
            except mysql.connector.Error as error:
                # Exclude selfmade trigger errors
                if error.sqlstate != "45000":
                    print("Something went wrong! {}".format(error), table_name)
                    print(entry)
        cursor.close()

    # TODO: accept multiple tables and dfs in one call
    def insertMany(self, table_name, df):
        cursor = self.mydb.cursor(prepared=True)
        try:
            cursor.executemany(self.sql_insert_dict[table_name], list(df.itertuples(index=False, name=None)))
        except mysql.connector.Error as error:
            # self.mydb.rollback()
            print("Something went wrong! {}".format(error), table_name)
        cursor.close()

    def selectTypeTable(self, table_name):
        match table_name:
            case "type_of_faculty":
                return pd.read_sql_query("SELECT FacultyID, FacultyType FROM type_of_faculty", self.mydb).replace({np.nan: None})
            case "type_of_expertise":
                return pd.read_sql_query("SELECT ExpertiseID, ExpertiseType FROM type_of_expertise", self.mydb).replace({np.nan: None})
            case "type_of_position":
                return pd.read_sql_query("SELECT PositionID, PositionType FROM type_of_position", self.mydb).replace({np.nan: None})
            case _:
                print("Invalid type table!")
                return None

    def getPersonMaxID(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT max(PersonID) FROM person")
        result = cursor.fetchone()[0]
        cursor.close()
        return result


# Main
if __name__ == "__main__":
    print("database.py")
