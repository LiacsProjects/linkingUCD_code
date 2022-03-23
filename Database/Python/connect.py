import mysql.connector

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
  (1, 'pieter', 'hendriks'),
]

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "record was inserted.")