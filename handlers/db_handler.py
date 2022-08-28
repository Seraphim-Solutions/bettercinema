import sqlite3

class db():
    def __init__(self):
        self.con = sqlite3.connect('config/data.db')
        self.cur = self.con.cursor()
        sql_create_storage_provider = """CREATE TABLE IF NOT EXISTS `webshare` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `username` tinytext,
  `hash` text
);

CREATE TABLE IF NOT EXISTS `trakt` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `access_token` tinytext,
  `refresh_token` tinytext,
  `expires_in` int,
  `created_at` int,
  `trakt_username` tinytext,
  `private` tinyint(1),
  `vip` tinyint(1),
  `vip_ep` tinyint(1),
  `slug` tinytext
);

CREATE TABLE IF NOT EXISTS `opensubtitles` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `username` tinytext NOT NULL,
  `hash` tinytext NOT NULL
);

CREATE TABLE IF NOT EXISTS `titulkycom` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `username` tinytext NOT NULL,
  `hash` tinytext NOT NULL
);"""




        self.con.executescript(sql_create_storage_provider)

    def add_creds(self, username, hash):
        self.cur.execute("INSERT INTO webshare (username, hash) VALUES (?, ?)", (username, hash))
        self.con.commit()
    

    def add_device_auth(self, access_token, refresh_token, expires_in, created_at, current_user):
        self.cur.execute("SELECT id FROM trakt")
        if self.cur.fetchone() is None:
            self.cur.execute("INSERT INTO trakt (access_token, refresh_token, expires_in, created_at) VALUES (?, ?, ?, ?)", (access_token, refresh_token, expires_in, created_at))
        else:
            self.cur.execute("UPDATE trakt SET access_token = ?, refresh_token = ?, expires_in = ?, created_at = ? WHERE id = ?", (str(access_token), str(refresh_token), int(expires_in), int(created_at), int(current_user)))
        self.con.commit()

    
    def add_trakt_user_data(self, username, private, vip, vip_ep, slug, current_user):
        # insert if empty or update if not
        self.cur.execute("SELECT id FROM trakt")
        if self.cur.fetchone() is None:
            self.cur.execute("INSERT INTO trakt (trakt_username, private, vip, vip_ep, slug) VALUES (?, ?, ?, ?, ?)", (username, private, vip, vip_ep, slug))
        else:
            self.cur.execute("UPDATE trakt SET trakt_username = ?, private = ?, vip = ?, vip_ep= ?, slug = ? WHERE id = ?", (username, private, vip, vip_ep, slug, current_user))
        self.con.commit()

    
    def read_creds(self):
        self.cur.execute("SELECT username, hash FROM webshare")
        return self.cur.fetchall()

    
    def read_device_auth(self):
        self.cur.execute("SELECT id, access_token, refresh_token, expires_in, created_at FROM trakt WHERE id = ?", (self.get_current_user()))
        return self.cur.fetchall()
    

    def read_trakt_user_data(self):
        self.cur.execute("SELECT trakt_username, private, vip, vip_ep, slug FROM trakt WHERE id = ?", (self.get_current_user())")
        return self.cur.fetchall()

    
    def get_current_user(self):
        self.cur.execute("SELECT id FROM webshare")
        return self.cur.fetchone()