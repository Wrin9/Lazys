import sqlite3

class Operational_DB:
    def __init__(self):
        self.conn = self.Initialize_the_check_database()

    def Initialize_the_check_database(self):
        db_name = 'Nscan.db'
        conn = sqlite3.connect(db_name)
        return conn
    
    def insert_data(self, table_name, data, code=None):
        cursor = self.conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS '{table_name}' (ip TEXT, port TEXT, title TEXT, host TEXT, country TEXT, province TEXT, city TEXT, url TEXT, code TEXT)")
        for i in data:
            url = f"{i['ip']}:{i['port']}"
            cursor.execute(f"INSERT INTO '{table_name}' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (i['ip'], i['port'], i['service']['http']['title'], i['service']['http']['host'],
                            i['location']['country_cn'], i['location']['province_cn'], i['location']['city_cn'], url, code))
            self.conn.commit()
