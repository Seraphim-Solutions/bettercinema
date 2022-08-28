import sqlite3

class db():
    def __init__(self):
        self.con = sqlite3.connect('config/data.db')
        self.cur = self.con.cursor()
        sql_create_projects_table = """CREATE TABLE IF NOT EXISTS user (
                                        username text,
                                        hash text,
                                        access_token text,
                                        refresh_token text,
                                        expires_in int,
                                        created_at int,
                                        trakt_username text,
                                        private bool,
                                        vip bool,
                                        vip_ep bool,
                                        slug text
                                    );"""

        self.con.execute(sql_create_projects_table)

    def add_creds(self, username, hash):
        self.cur.execute("INSERT INTO user (username, hash) VALUES (?, ?)", (username, hash))
        self.con.commit()
    

    def add_device_auth(self, access_token, refresh_token, expires_in, created_at, current_user):
        self.cur.execute("UPDATE user SET access_token = ?, refresh_token = ?, expires_in = ?, created_at = ? WHERE username = ?", (access_token, refresh_token, expires_in, created_at, current_user))
        self.con.commit()

    
    def add_trakt_user_data(self, username, private, vip, vip_ep, slug, current_user):
        self.cur.execute("UPDATE user SET trakt_username = ?, private = ?, vip = ?, vip_ep= ?, slug = ? WHERE username = ?", (username, private, vip, vip_ep, slug, current_user))
        self.con.commit()

    
    def read_creds(self):
        self.cur.execute("SELECT username, hash FROM user")
        return self.cur.fetchall()

    
    def read_device_auth(self):
        self.cur.execute("SELECT access_token, refresh_token, expires_in, created_at FROM user")
        return self.cur.fetchall()
    

    def read_trakt_user_data(self):
        self.cur.execute("SELECT trakt_username, private, vip, vip_ep, slug FROM user")
        return self.cur.fetchall()