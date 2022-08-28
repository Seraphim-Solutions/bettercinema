from textwrap import wrap
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import os
from rich import print, pretty
from rich.console import Console
from rich.traceback import install
from rich.table import Table
import xml.etree.ElementTree as ET
import hashlib
import json
import time

from api.api import BetterCinemaAPI
from handlers.request_parser import Handler
from handlers.vlc_handler import Player
from handlers.infuse_handler import Player_Infuse
from misc.md5Crypt import md5Crypt
from handlers.db_handler import db
from handlers.config_handler import ConfigHandler
from handlers.trakt.oauth import oauth


class Cli():
    def __init__(self):
        ConfigHandler()
        self.bc = BetterCinemaAPI()
        self.rp = Handler()
        self.player = Player()
        self.player_infuse = Player_Infuse()
        self.db = db()
        self.md5crypt = md5Crypt()
        self.trakt_oauth = oauth()
        self.movie_names, self.movie_idents, self.movie_sizes, self.movie_postive_votes, self.movie_negative_votes = [], [], [], [], []
        self.movie_links = []
        self.page = 0
        self.user_dict = {}
        users = self.db.read_creds()
        self.has_trakt_auth = None
        self.clear = os.system('cls' if os.name == 'nt' else 'clear')
        if users != []:
            for username, hash in users:
                self.user_dict.update({username: hash})
        
        with open('config/config.json', 'r') as f:
            self.config = json.load(f)
        
        self.color_neutral = self.config['colors']['neutral']
        self.color_good = self.config['colors']['good']
        self.color_bad = self.config['colors']['bad']
        self.color_warning = self.config['colors']['warning']
        self.color_info = self.config['colors']['info']
        self.color_primary = self.config['colors']['primary']
    
    def get_salt(self, username):
        salt_xml = self.rp.salt(username)
        xml = ET.fromstring(salt_xml)
        if not xml.find('status').text == 'OK':
            print("User not found.")
            self.login()
        else:
            pass
        salt = xml.find('salt').text
        return salt

    def get_wst(self, username, password):
        wst_xml = self.rp.login(username, password)
        xml = ET.fromstring(wst_xml)
        
        if not xml.find('status').text == 'OK':
            print("Invalid credentials.")
            self.login()
            
        self.wst = xml.find('token').text

    def get_password_hash(self, password, salt):
        return hashlib.sha1(self.md5crypt.md5crypt(pw=password, salt=salt).encode('utf-8')).hexdigest()
    
    def stored_account(self):
        use_sotred_account = inquirer.confirm(message="Use stored account?: ").execute()
        if use_sotred_account:
            user_choice = inquirer.select(message="Choose account: ", choices=[
                *self.user_dict
            ]).execute()

            username = user_choice
            password = self.user_dict[username]
            
            return username, password

        if use_sotred_account == False:
            username = inquirer.text(message="Username: ").execute()
            salt = self.get_salt(username)
            password = inquirer.secret(message="Password: ").execute()
            self.get_wst(username, self.get_password_hash(password, salt))
            return username, password

    def login(self):
        if self.db.read_creds() == []:
            username = inquirer.text(message="Username: ").execute()
            password = inquirer.secret(message="Password: ").execute()
            salt = self.get_salt(username)
            self.get_wst(username, self.get_password_hash(password, salt))

        else:
            username, password = self.stored_account()
        
        if username not in self.user_dict.keys():
            self.db.add_creds(username, self.get_password_hash(password, salt))
        self.clear
        self.search()

    
    def search_query(self, query: dict):
        self.resutl_list = self.bc.search(query)
        if self.resutl_list == None:
            print(f"[{self.color_info}] > No results found[/]\n")
            self.search()

    def search(self):
            search_type = inquirer.select(message="Options: ", choices=[
                "Default Search",
                "Advanced Search",
                "Open Link",
                Choice("Trakt.tv", "Trakt.tv [Beta]")],
                default="Default Search").execute()
            if search_type == "Default Search":
            # seach for movies with self.bc and print movies
                query = inquirer.text(message="Search for movie: ").execute()
                
                self.query_dict = {"what": query, "offset": 0, "limit": 25, "category": "video", "sort": "largest"}
                self.search_query(self.query_dict)
                self.list_movies()
            if search_type == "Advanced Search":
                self.advanced_search()

            if search_type == "Open Link":
                link = inquirer.text(message="Link: ").execute()
                self.player.play(link)

            if search_type == "Trakt.tv":
                print("This functionality is not yet implemented.")
                self.trakt_auth() if self.has_trakt_auth == None else self.search() # temp until trakt handler is implemented | move this to trakt_tv() after trakt handler is implemented
                #self.trakt_tv()

    def advanced_search(self):
        query = inquirer.text(message="Name: ").execute()
        limit = inquirer.text(message="Limit [defaul is 25]: ").execute()
        offset = 0
        category = inquirer.fuzzy(message="Category [default is video]: ", choices=[
            "video",
            "audio",
            "images",
            "archives",
            "docs",
            "software",
            "adult"]).execute()
        sort = inquirer.fuzzy(message="Sort [default is largest]: ", choices=[
            "largest",
            "smallest",
            "recent",
            Choice("", "relevance"),
            "rating"
            ]).execute()

        self.query_dict = {"what": query, "offset": offset, "limit": int(limit), "category": category, "sort": sort}

        self.search_query(self.query_dict)
        self.list_movies()

    def get_result_data(self):
        for movie in self.resutl_list:  
            self.movie_idents.append(movie[0])
            self.movie_names.append(movie[1])
            self.movie_sizes.append(movie[2])
            self.movie_postive_votes.append(movie[3])
            self.movie_negative_votes.append(movie[4])
        return

    def list_movies(self):
        self.get_result_data()
        self.movie_table = Table(show_header=True, header_style=self.color_neutral, title="Search Results", title_justify="centre")
        self.movie_table.add_column("#", style=self.color_primary, justify="middle")
        self.movie_table.add_column("Name", style=self.color_good, justify="middle")
        self.movie_table.add_column("Size", style=self.color_warning, justify="middle")
        self.movie_table.add_column("Votes", justify="middle", no_wrap=True)
        for i in range(len(self.movie_names)):
            self.movie_table.add_row(f"[{self.color_primary}]{str(i + 1)}[/]",
            self.movie_names[i],
            f"[{self.color_warning}]{self.movie_sizes[i]}[/]",
            (f"[{self.color_good}]{self.movie_postive_votes[i]}[/] [{self.color_neutral}]|[/] [{self.color_bad}]{self.movie_negative_votes[i]}[/]"),
            style=(self.color_neutral if self.movie_postive_votes[i] == self.movie_negative_votes[i] else ("bold" if self.movie_postive_votes[i] >= self.movie_negative_votes[i] else self.color_bad)))

        console.print(self.movie_table)
        self.select_item_from_results()

    def select_item_from_results(self):
        selected_movie = inquirer.text(message="Select movie [help for options]: ").execute()
        if selected_movie == "help":
            self.help()
        if selected_movie == "more":
            self.more_results()
        

        selected_movie_index = int(selected_movie) - 1

        movie_link = self.bc.get_link(ident=self.movie_idents[selected_movie_index], wst=self.wst)
        if movie_link == "Error 403":
            print("No link found, maybe the file is password protected.")
            self.select_item_from_results()
        else:
            self.selected_item_options(movie_link)
        
    def selected_item_options(self, movie_link):
        item_options = inquirer.select(message="Select item options: ", choices=[
            "Download",
            "Get Link",
            "Play in VLC [Network Stream]",
            "Play in Infuse [Apple only]"]).execute()
        
        if item_options == "Download":
            filename = inquirer.text(message="Filename: ").execute()
            self.rp.download(filename, movie_link)
            self.search()

        if item_options == "Play in VLC [Network Stream]":
            self.player.play(movie_link)
            
        if item_options == "Play in Infuse [Apple only]":
            self.player_infuse.play(movie_link)

        if item_options == "Get Link":
            print(movie_link)
            self.search()

    def trakt_tv_movies(self):
        movies_options = inquirer.fuzzy(message="Options: ", choices=[
            "Trending",
            "Popular",
            "Recommended",
            "Watched",
            "Collected",
            "Anticipated",
            "Box Office"]).execute()

    def trakt_tv_shows(self):
        shows_options = inquirer.fuzzy(message="Options: ", choices=[
            "Trending",
            "Popular",
            "Recommended",
            "Watched",
            "Collected",
            "Anticipated"]).execute()

    def trakt_tv(self):
        video_type = inquirer.select(message="Options: ", choices=[
            "Movies",
            "TV Shows"],
            default="Movies").execute()

        if video_type == "Movies":
            self.trakt_tv_movies()
        if video_type == "TV Shows":
            self.trakt_tv_shows()


    def trakt_auth(self):
        if self.db.read_device_auth() == []:
            auth_code = self.trakt_oauth.authorize_device()
            print(f"Please go to the following URL and enter the code: [bold]{auth_code[0]}[/]\n{auth_code[1]}")
            input("Press enter to continue, after you athorize...")
            self.trakt_oauth.get_device_token(auth_code[2])
            self.trakt_oauth.get_settings()
        else:
            print(f"Already authorized as {self.db.read_trakt_user_data()[0][0]}")

    def more_results(self):
        self.page += 25
        self.query_dict['offset'] = self.page
        self.resutl_list = self.bc.search(self.query_dict)
        self.list_movies()

    def help(self):
        print("Select movie by typing the number of the movie or 'more' for more results")
        self.select_item_from_results()

if __name__ == '__main__':
    os.system("title BetterCinema")
    pretty.install()
    install()
    console = Console()
    os.system('cls' if os.name == 'nt' else 'clear')
    app = Cli()
    app.login()