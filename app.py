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

from api.api import BetterCinemaAPI
from handlers.request_parser import Handler
from handlers.vlc_handler import Player
from misc.md5Crypt import md5crypt
from handlers.db_handler import db



class Cli():
    def __init__(self):
        self.bc = BetterCinemaAPI()
        self.rp = Handler()
        self.player = Player()
        self.db = db()
        self.movie_names = []
        self.movie_idents = []
        self.movie_sizes = []
        self.movie_postive_votes = []
        self.movie_negative_votes = []
        self.movie_links = []
        self.page = 0
        # load config/config.json
        with open('config/config.json') as config_file:
            self.config = json.load(config_file)
        self.color_neutral = self.config['colors']['neutral']
        self.color_good = self.config['colors']['good']
        self.color_bad = self.config['colors']['bad']
        self.color_warning = self.config['colors']['warning']
        self.color_info = self.config['colors']['info']
        self.color_primary = self.config['colors']['primary']

    def login(self):
        if self.db.read_creds() == []:
            username = inquirer.text(message="Username: ").execute()
            password = inquirer.secret(message="Password: ").execute()
            salt_xml = self.rp.salt(username)
            xml = ET.fromstring(salt_xml)
            if not xml.find('status').text == 'OK':
                print("User not found.")
                self.login()
            else:
                pass
            salt = xml.find('salt').text
            password = hashlib.sha1(md5crypt(password, salt=salt).encode('utf-8')).hexdigest()
        else:
            use_logged_account = inquirer.text(message=f"You have already logged in as {self.db.read_creds()[0][0]}. Do you want to use this account? [y/n]: ").execute()
            if use_logged_account == "y":
                username = self.db.read_creds()[0][0]
                password = self.db.read_creds()[0][1]
            if use_logged_account == "n":
                username = inquirer.text(message="Username: ").execute()
                password = inquirer.secret(message="Password: ").execute()
                salt_xml = self.rp.salt(username)
                xml = ET.fromstring(salt_xml)
                salt = xml.find('salt').text
                password = hashlib.sha1(md5crypt(password, salt=salt).encode('utf-8')).hexdigest()
        
        wst_xml = self.rp.login(username, password)
        xml = ET.fromstring(wst_xml)
        
        if not xml.find('status').text == 'OK':
            print("Invalid credentials.")
            self.login()
            
        self.wst = xml.find('token').text
        if self.db.read_creds() != [(username, password)]:
            self.db.add_creds(username, password)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.search()

    def search_query(self, query, limit=25, category="video", sort="largest", offset=0):
        self.query = query
        self.resutl_list = self.bc.search(self.query, limit=limit, category=category, offset=offset, sort=sort)
        

    def search(self):
            search_type = inquirer.select(message="Search options: ", choices=[
                "Default Search",
                "Advanced Search"],
                default="Default Search").execute()
            if search_type == "Default Search":
            # seach for movies with self.bc and print movies
                query = inquirer.text(message="Search for movie: ").execute()
                self.search_query(query)
                self.list_movies()
            else:
                self.advanced_search()
    
    def advanced_search(self):
        query = inquirer.text(message="Name: ").execute()
        limit = inquirer.text(message="Limit [defaul is 25]: ").execute()
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

        self.search_query(query, int(limit), category, sort)
        self.list_movies()

    def list_movies(self):
        for movie in self.resutl_list:
            self.movie_idents.append(movie[0])
            self.movie_names.append(movie[1])
            self.movie_sizes.append(movie[2])
            self.movie_postive_votes.append(movie[3])
            self.movie_negative_votes.append(movie[4])
        
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
        self.selected_item_options(movie_link)
        
    def selected_item_options(self, movie_link):
        item_options = inquirer.select(message="Select item options: ", choices=[
            "Download",
            "Play in VLC [Network Stream]"]).execute()
        
        if item_options == "Download":
            filename = inquirer.text(message="Filename: ").execute()
            self.rp.download(filename, movie_link)
            self.search()

        if item_options == "Play in VLC [Network Stream]":
            self.player.play(movie_link)


    def more_results(self):
        self.page += 25
        self.resutl_list = self.bc.search(self.query, category="video", limit=25, offset=self.page)
        self.list_movies()

    def help(self):
        print("Select movie by typing the number of the movie or 'more' for more results")
        self.select_item_from_results()

if __name__ == '__main__':
    pretty.install()
    install()
    console = Console()
    os.system('cls' if os.name == 'nt' else 'clear')
    app = Cli()
    app.login()