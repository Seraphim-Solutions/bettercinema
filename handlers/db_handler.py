import sqlite3

class db():
    def __init__(self):
        self.con = sqlite3.connect('config/data.db')
        self.cur = self.con.cursor()
        sql_create_projects_table = """CREATE TABLE IF NOT EXISTS creds (
                                        username text NOT NULL,
                                        hash text NOT NULL
                                    );"""

        self.con.execute(sql_create_projects_table)

    def add_creds(self, username, hash):
        self.cur.execute("INSERT INTO creds VALUES (?, ?)", (username, hash))
        self.con.commit()
    
    def read_creds(self):
        self.cur.execute("SELECT * FROM creds")
        return self.cur.fetchall()