import sqlite3

class DB_Manager:
    db_name: str
    table_name: str
    connection = None
    cursor = None

    def __init__(self, db_name, table_name):
        self.db_name = db_name
        self.table_name = table_name
    
    def change_table(self, table_name):
        self.table_name = table_name
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()

    def insert_user(self, args):
        customer_number, fname, lname, gender, birth_date = args
        sql_command = f'INSERT INTO {self.table_name} (customer_number, fname, lname, gender, birth_date) VALUES ({customer_number}, \"{fname}\", \"{lname}\", \"{gender}\", \"{birth_date}\");'
        self.cursor.execute(sql_command)
        self.connection.commit()
    
    def update_user(self, args):
        customer_number, colname, new_val = args
        sql_command = f"UPDATE {self.table_name} SET {colname} = \"{new_val}\" WHERE customer_number = {customer_number}"
        self.cursor.execute(sql_command)
        self.connection.commit()

    def show_user(self, customer_number):
        sql_command = f"SELECT * FROM {self.table_name} where customer_number = {customer_number}"
        self.cursor.execute(sql_command)
        print(self.cursor.fetchone())
    
    def show_all_users(self):
        sql_command = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(sql_command)
        print(self.cursor.fetchall())
    
    def delete_user(self, customer_number):
        sql_command = f"DELETE FROM {self.table_name} where customer_number = {customer_number}"
        self.cursor.execute(sql_command)
        self.connection.commit()
    
if __name__ == "__main__":
    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    DB.insert_user((3, "Sercan", "Berg", "m", "2000-08-17"))
    DB.show_all_users()
    DB.update_user((2, "lname", "Testo"))
    DB.show_all_users()
    DB.delete_user(2)
    DB.show_all_users()
