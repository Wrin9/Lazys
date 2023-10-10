import sqlite3
import threading

class Operational_DB:
    def __init__(self):
        self.conn = self.Initialize_the_check_database()
        self.lock = threading.Lock()

    def Initialize_the_check_database(self):
        db_name = 'Nscan.db'
        conn = sqlite3.connect(db_name, check_same_thread=False)
        return conn
    
    def insert_data(self, table_name, data, code=None):
        cursor = self.conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS '{table_name}' (ip TEXT, port TEXT, title TEXT, host TEXT, country TEXT, province TEXT, city TEXT, url TEXT, code TEXT)")
        
        def insert_rows(rows):
            local_conn = sqlite3.connect('Nscan.db', check_same_thread=False)
            local_cursor = local_conn.cursor()
            for row in rows:
                url = f"{row['ip']}:{row['port']}"
                local_cursor.execute(f"INSERT INTO '{table_name}' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                    (row['ip'], row['port'], row['service']['http']['title'], row['service']['http']['host'],
                                     row['location']['country_cn'], row['location']['province_cn'], row['location']['city_cn'], url, code))
            local_conn.commit()
            local_conn.close()
        
        threads = []
        group_size = 100
        for i in range(0, len(data), group_size):
            group = data[i:i+group_size]
            thread = threading.Thread(target=insert_rows, args=(group,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
