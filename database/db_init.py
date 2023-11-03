import sqlite3
connection = sqlite3.connect("kundendatenbank.sql")
cursor = connection.cursor()
 
#cursor.execute("""DROP TABLE users;""")

sql_command = """
CREATE TABLE users ( 
customer_number INTEGER PRIMARY KEY, 
fname VARCHAR(20), 
lname VARCHAR(30), 
gender CHAR(1), 
joining DATE,
birth_date DATE);"""
cursor.execute(sql_command)

sql_command = """INSERT INTO users (customer_number, fname, lname, gender, birth_date)
    VALUES (NULL, "William", "Shakespeare", "m", "1961-10-25");"""
cursor.execute(sql_command)

sql_command = """INSERT INTO users (customer_number, fname, lname, gender, birth_date)
    VALUES (NULL, "Frank", "Schiller", "m", "1955-08-17");"""
cursor.execute(sql_command)

connection.commit()
connection.close()