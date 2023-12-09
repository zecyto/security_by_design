import sqlite3

class DB_LogManager:
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

    def insert_log_entry(self, args):
        log_id, editor_account, role, target_account, timestamp, mac = args
        sql_command = f'INSERT INTO {self.table_name} (log_id, editor_account, role, target_account, timestamp, mac) VALUES ({log_id}, \"{editor_account}\", \"{role}\", \"{target_account}\", \"{timestamp}\", \"{mac}\");'
        self.cursor.execute(sql_command)
        self.connection.commit()

    def show_all_logs(self):
        sql_command = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(sql_command)
        print(self.cursor.fetchall())
    
    def get_all_logs(self):
        sql_command = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(sql_command)
        all_logs = self.cursor.fetchall()
        res = []
        for log in all_logs:
            log_dict = {"editor_account": log[1], "role": log[2], "target_account": log[3], "timestamp": log[4], "mac": log[5]}
            res.append(log_dict)
        return res