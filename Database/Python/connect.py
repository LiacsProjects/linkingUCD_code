import mysql.connector
import pandas as pd
from faker import Faker
from collections import defaultdict
from sqlalchemy import create_engine
fake = Faker()
fake_data = defaultdict(list)
for _ in range(1000):
  fake_data["Firstname"].append(fake.first_name())
  fake_data["Lastname"].append(fake.last_name())

df_fake_data = pd.DataFrame(fake_data)

print(df_fake_data)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  database="LUCD",
  port="3306"
)

mycursor = mydb.cursor()

sql = "INSERT INTO person (PersonID, Firstname, Lastname) VALUES (%s, %s, %s)"
val = [
  (),
]

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "record was inserted.")