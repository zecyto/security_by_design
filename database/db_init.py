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
role VARCHAR(10) DEFAULT "user",
fname VARCHAR(20), 
lname VARCHAR(30), 
joining DATE,
password VARCHAR(64),
salt VARCHAR(64),
mfa VARCHAR(64) NULL,
failed_login INTEGER DEFAULT 0);"""
cursor.execute(sql_command)

sql_command = """INSERT INTO users (customer_number, email, role, fname, lname, joining, password, salt, mfa)
    VALUES (NULL, 'admin@admin', 'admin', 'admin', 'admin', '2023-12-03', '468d59c4ee389f925c2f9e7d4da9521f1365357f497bfe4fb2989ffd4b66e13c', '03203557143c25249fac141445996a88eee43e0046cae0b3f9d1922478191775', 'FJMXJNVZSYV5A4PFOIWC5MXQO5KSMUOT');"""
cursor.execute(sql_command)


connection.commit()
connection.close()