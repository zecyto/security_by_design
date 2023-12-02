import sqlite3
connection = sqlite3.connect("database/kundendatenbank.sql")
cursor = connection.cursor()

try:
    cursor.execute("""DROP TABLE users;""")
except:
    pass

sql_command = """
CREATE TABLE users ( 
customer_number INTEGER PRIMARY KEY,
email VARCHAR(30),
fname VARCHAR(20), 
lname VARCHAR(30), 
joining DATE,
password VARCHAR(64),
salt VARCHAR(64),
mfa VARCHAR(64) NULL);"""
cursor.execute(sql_command)

sql_command = """INSERT INTO users (customer_number, email, fname, lname, joining, password, salt)
    VALUES (NULL, "William@S", "William", "Shakespeare", "1961-10-25", "abcdef12345", "abc");"""
cursor.execute(sql_command)

sql_command = """INSERT INTO users (customer_number, email, fname, lname, joining, password, salt)
    VALUES (NULL, "Frank@S", "Frank", "Schiller", "1961-10-25", "abcdef12345", "abc");"""
cursor.execute(sql_command)

connection.commit()
connection.close()