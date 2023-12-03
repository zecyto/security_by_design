import sqlite3
import secrets

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

    def insert_user(self, args, random_hex = None):
        customer_number, email, fname, lname, joining, password = args
        if not random_hex:
            random_hex = secrets.token_hex(32)
        sql_command = f'INSERT INTO {self.table_name} (customer_number, email, fname, lname, joining, password, salt) VALUES ({customer_number}, \"{email}\", \"{fname}\", \"{lname}\", \"{joining}\", \"{password}\", \"{random_hex}\");'
        self.cursor.execute(sql_command)
        self.connection.commit()
    
    def update_user(self, args):
        customer_number, colname, new_val = args
        sql_command = f"UPDATE {self.table_name} SET {colname} = \"{new_val}\" WHERE customer_number = {customer_number}"
        self.cursor.execute(sql_command)
        self.connection.commit()

    def get_user(self, customer_number):
        sql_command = f"SELECT * FROM {self.table_name} where customer_number = {customer_number}"
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()
    
    def get_login_data_by_mail(self, mail):
        sql_command = f"SELECT password, salt, customer_number FROM {self.table_name} where email = \"{mail}\""
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()

    def get_mail_and_name_by_id(self, id):
        sql_command = f"SELECT email, fname FROM {self.table_name} where customer_number = {id}"
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()

    def get_mfa_by_id(self, id):
        sql_command = f"SELECT mfa FROM {self.table_name} where customer_number = {id}"
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()

    def get_id_by_mail(self, mail):
        sql_command = f"SELECT customer_number FROM {self.table_name} where email = \"{mail}\""
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()
    
    def get_role_by_id(self, id):
        sql_command = f"SELECT role FROM {self.table_name} where customer_number = {id}"
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()
    
    def set_admin(self, id, colname = "role", new_val = "admin"):
        sql_command = f"UPDATE {self.table_name} SET {colname} = \"{new_val}\" WHERE customer_number = {id}"
        self.cursor.execute(sql_command)
        self.connection.commit()


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
    #DB.insert_user(("NULL", "Sercan@B", "Sercan", "Berg", "2000-08-17", "1234567abc"))
    #DB.show_all_users()
    #DB.update_user((2, "lname", "Testo"))
    #DB.show_all_users()
    #DB.update_user((3, "role", "Testo"))
    #DB.get_login_data_by_mail("William@S")
    #DB.delete_user(2)
    DB.show_all_users()
