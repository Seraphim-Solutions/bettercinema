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
import sys

from api.api import BetterCinemaAPI
from handlers.request_parser import Handler
from handlers.vlc_handler import Player
from handlers.infuse_handler import Player_Infuse
from misc.md5Crypt import md5Crypt
from handlers.db_handler import db
from handlers.config_handler import ConfigHandler
from handlers.trakt_handler import Trakt 

class Cli():
    def __init__(self):
        ConfigHandler()
        self.bc = BetterCinemaAPI()
        self.rp = Handler()
        self.player = Player()
        self.player_infuse = Player_Infuse()
        self.db = db()
        self.md5crypt = md5Crypt()
        self.Trakt = Trakt()
        self.clear_table_data()
        self.movie_links = []
        self.page = 0
        self.user_dict = {}
        users = self.db.read_creds()
        self.has_trakt_auth = None
        if users != []:
            for username, hash in users:
                self.user_dict.update({username: hash})
        
        with open('config/config.json', 'r') as f:
            self.config = json.load(f)
        self.load_colors()

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def clear_table_data(self):
        self.movie_names, self.movie_idents, self.movie_sizes, self.movie_postive_votes, self.movie_negative_votes = [], [], [], [], []

    def load_colors(self, theme='default'):
        self.color_neutral = self.config['colors'][theme]['neutral']
        self.color_good = self.config['colors'][theme]['good']
        self.color_bad = self.config['colors'][theme]['bad']
        self.color_warning = self.config['colors'][theme]['warning']
        self.color_info = self.config['colors'][theme]['info']
        self.color_primary = self.config['colors'][theme]['primary']
        self.color_banner = self.config['banner']['color']

    def settings(self):
        themes = [theme for theme in self.config['colors']]
        options = inquirer.select(message="Color Theme: ", choices=[*themes]).execute()
        
        if options:
            self.load_colors(options)
            self.menu()

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
        use_sotred_account = inquirer.confirm(message="Use stored account?: ", default=True).execute()
        if use_sotred_account:
            user_choice = inquirer.select(message="Choose account: ", choices=[
                *self.user_dict
            ]).execute()

            username = user_choice
            password = self.user_dict[username]
            self.get_wst(username, password)
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
            salt = self.get_salt(username)
            self.db.add_creds(username, self.get_password_hash(password, salt))
        
        self.db.get_current_user()
        self.username = username
        self.clear_console()
        self.menu()

    
    def search_query(self, query: dict):
        self.resutl_list = self.bc.search(query)
        if self.resutl_list == None:
            print(f"[{self.color_info}] > No results found[/]\n")
            self.menu()

    def menu(self):
        self.clear_table_data()
        print(f"[{'blink ' + self.color_banner if self.config['banner']['animation'] == 1 else self.color_banner}]{self.config['banner']['text']}[/]\n          🎬 [i]DanniSec's & Trivarialthea's Project[/] 🎬\n")
        search_type = inquirer.select(message="Options: ", choices=[
            "Default Search",
            "Advanced Search",
            "Open Link",
            Choice("Trakt.tv", "Trakt.tv [Beta]"),
            "Settings"],
            default="Default Search").execute()
        
        if search_type == "Default Search":
            self.clear_console()
        # seach for movies with self.bc and print movies
            query = inquirer.text(message="Search for movie: ").execute()
            
            self.query_dict = {"what": query, "offset": 0, "limit": 25, "category": "video", "sort": ""}
            self.search_query(self.query_dict)
            self.list_movies(query, sort="")
        
        if search_type == "Advanced Search":
            self.clear_console()
            self.advanced_search()
        
        if search_type == "Open Link":
            self.clear_console()
            link = inquirer.text(message="Link: ").execute()
            self.player.play(link)
            
        if search_type == "Trakt.tv":
            self.clear_console()
            print("This functionality is not yet implemented.")
            #self.trakt_auth() if self.has_trakt_auth == None else self.menu() # temp until trakt handler is implemented | move this to trakt_tv() after trakt handler is implemented
            #self.trakt_tv()
        
        if search_type == "Settings":
            self.clear_console()
            self.settings()

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
        self.list_movies(query, sort)

    def get_result_data(self):
        for movie in self.resutl_list:  
            self.movie_idents.append(movie[0])
            self.movie_names.append(movie[1])
            self.movie_sizes.append(movie[2])
            self.movie_postive_votes.append(movie[3])
            self.movie_negative_votes.append(movie[4])
        return

    def list_movies(self, query, sort):
        self.get_result_data()
        
        self.movie_table = Table(show_header=True, header_style=self.color_neutral, title=f'Search Results for \"{query}\" | sort by: {"relevance" if sort == "" else sort}', title_justify="center")
        self.movie_table.add_column("#", style=self.color_primary, justify="middle")
        self.movie_table.add_column("Name", style=self.color_good, justify="middle")
        self.movie_table.add_column("Size", style=self.color_warning, justify="middle")
        self.movie_table.add_column("Votes", justify="middle", no_wrap=True)
        for i in range(len(self.movie_names)):
            self.movie_table.add_row(f"[{self.color_primary}]{str(i + 1)}[/]",
            self.movie_names[i],
            f"[{self.color_warning}]{self.movie_sizes[i]}[/]",
            (f"[{self.color_good}]{self.movie_postive_votes[i]}[/] [{self.color_neutral}]|[/] [{self.color_bad}]{self.movie_negative_votes[i]}[/]"),
            style=(self.color_neutral if self.movie_postive_votes[i] == self.movie_negative_votes[i] else ("" if self.movie_postive_votes[i] >= self.movie_negative_votes[i] else self.color_bad)))

        console.print(self.movie_table)
        self.select_item_from_results()


    def select_item_from_results(self):
        selected_movie = inquirer.text(message="~> ").execute()
        commands = ("help", "more", "search", "sort", "menu", "exit")

        if selected_movie not in commands and selected_movie.isdigit() and int(selected_movie) <= len(self.movie_names):
            selected_movie_index = int(selected_movie) - 1

            movie_link = self.bc.get_link(ident=self.movie_idents[selected_movie_index], wst=self.wst)
            if movie_link == "Error 403":
                print("No link found, maybe the file is password protected.")
                self.select_item_from_results()
            else:
                self.selected_item_options(movie_link)

        if selected_movie == "help":
            self.help()
        
        if selected_movie == "more":
            self.clear_console()
            self.more_results()
        
        if "sort " in selected_movie:
            self.page = 0
            self.query_dict['offset'] = self.page
            self.clear_console()
            self.clear_table_data()
            self.query_dict["sort"] = selected_movie.split(" ")[1]
            self.search_query(self.query_dict)
            self.list_movies(self.query_dict["what"], self.query_dict["sort"])

        if "search " in selected_movie:
            self.clear_console()
            self.clear_table_data()
            self.query_dict["what"] = selected_movie.replace("search ", "")
            self.search_query(self.query_dict)
            self.list_movies(self.query_dict["what"], self.query_dict["sort"])

        if selected_movie == "menu":
            self.clear_console()
            self.menu()
        
        if selected_movie == "exit":
            self.clear_console()
            # close program
            sys.exit()

        else:
            print("Invalid input.")
            self.help()
            self.select_item_from_results()
        
        
    def selected_item_options(self, movie_link):
        item_options = inquirer.select(message="Select item options: ", choices=[
            "Download",
            "Get Link",
            "Play in VLC [Network Stream]",
            "Play in Infuse [Apple only]"]).execute()
        
        if item_options == "Download":
            filename = inquirer.text(message="Filename: ").execute()
            self.rp.download(filename, movie_link)
            self.select_item_from_results()

        if item_options == "Play in VLC [Network Stream]":
            self.player.play(movie_link)
            self.select_item_from_results()

        if item_options == "Play in Infuse [Apple only]":
            self.player_infuse.play(movie_link)
            self.select_item_from_results()

        if item_options == "Get Link":
            print(movie_link)
            self.select_item_from_results()


    def trakt_tv_movies(self):
        movies_options = inquirer.fuzzy(message="Options: ", choices=[
            Choice("trending", "Trending"),
            Choice("popular", "Popular"),
            Choice("recommended", "Recommended"),
            Choice("watched", "Watched"),
            Choice("collected", "Collected"),
            Choice("anticipated", "Anticipated"),
            Choice("box_office", "Box Office")]).execute()
        
        
        if movies_options:
            print(self.Trakt.movies(movies_options))


    def trakt_episodes(self, episodes):
        episode_name = [episode['title'] for episode in episodes]
        episode_number = [episode_count for episode_count in range(1, len(episode_name) + 1)]
        choices = [Choice(str(episode_number[i]), f"E:{episode_number[i]} {episode_name[i]}") for i in range(len(episode_name))]

        episode = inquirer.fuzzy(message="Select episode: ", choices=choices).execute()
        name = self.selcted_slug.replace("-", ".")
        query = f"{name}.S{int(self.season_selection):02d}E{int(episode):02d}"
        self.query_dict = {"what": query, "offset": 0, "limit": 25, "category": "video", "sort": ""}
        self.search_query(self.query_dict)
        self.list_movies()

    
    def trakt_season_list(self, seasons, slug):
        season_list = [Choice(season, f"Season {season}") for season in range(seasons)]
        
        self.season_selection = inquirer.fuzzy(message="Select season: ", choices=season_list).execute()
        
        episodes = self.Trakt.seasons(slug, self.season_selection)
        self.trakt_episodes(episodes)

    
    def search_trakt_seasons(self, query_list):
        choices = [Choice(self.slug[x], query_list[x]) for x in range(len(self.slug))]
        selection = inquirer.fuzzy(message="Select show: ", choices=[
                *choices
                ]).execute()
        seasons = self.Trakt.seasons(selection)
        self.selcted_slug = selection
        self.trakt_season_list(len(seasons), selection)


    def trakt_tv_shows(self):
        shows_options = inquirer.fuzzy(message="Options: ", choices=[
            Choice("trending", "Trending"),
            Choice("popular", "Popular"),
            Choice("recommended", "Recommended"),
            Choice("watched", "Watched"),
            Choice("collected", "Collected"),
            Choice("anticipated", "Anticipated")]).execute()


        if "popular" == shows_options:
            query_list = []
            show_list = ([[title['title'], title['ids']['slug'], title['year']] for title in self.Trakt.shows(shows_options, "90000")])
            [query_list.append(show[0]) for show in show_list]
            self.slug = [show[1] for show in show_list]

        else:
            query_list = []
            show_list = ([[title['show']['title'], title['show']['ids']['slug'], title['show']['year']] for title in self.Trakt.shows(shows_options, "90000")])
            [query_list.append(show[0]) for show in show_list]
            self.slug = [show[1] for show in show_list]
            
        self.search_trakt_seasons(query_list)
        

    def trakt_tv(self):
        option = inquirer.select(message="Options: ", choices=[
            "Search",
            "Movies",
            "TV Shows",
            "User"],
            default="Search").execute()

        if option == "Movies":
            self.trakt_tv_movies()
        if option == "TV Shows":
            self.trakt_tv_shows()
        if option == "User":
            self.trakt_user()
        if option == "Search":
            self.trakt_search()


    def trakt_user(self):
        user_options = inquirer.fuzzy(message="Options: ", choices=[
            Choice("history", "History"),
            Choice("watched", "Watched")]).execute()

        if user_options:
            if user_options == "watched":
                arg = inquirer.fuzzy(message="Type: ", choices=[
                    "movies",
                    "shows"]).execute()
                print(self.Trakt.user(user_options, self.db.read_trakt_user_data()[0][4], arg))
        print(self.Trakt.user(user_options, self.db.read_trakt_user_data()[0][4]))


    def trakt_auth(self):
        current_user = self.db.get_current_user()
        if str(current_user) not in str(self.db.read_device_auth()[0][0]):
            auth_code = self.Trakt.authorize_device()
            print(f"Please go to the following URL and enter the code: [bold]{auth_code[0]}[/]\n{auth_code[1]}")
            input("Press enter to continue, after you authorize...")
            self.Trakt.get_device_token(auth_code[2])
            self.Trakt.get_settings()
        else:
            print(f"Already authorized as {self.db.read_trakt_user_data()[0][0]}")
            self.trakt_tv()


    def trakt_search(self):
        search = inquirer.text(message="Search: ").execute()
        search_type = inquirer.fuzzy(message="Type: ", choices=[
            Choice("", "none"),
            "movie",
            "show",
            "episode",
            "person",
            "list"]).execute()

        print(self.Trakt.search(search, search_type))


    def more_results(self):
        self.page += 25
        self.query_dict['offset'] = self.page
        self.resutl_list = self.bc.search(self.query_dict)
        self.list_movies(self.query_dict["what"], self.query_dict["sort"])

    def help(self):
        print("Select movie by typing the # (number) of the movie. \
        \n'[b]more[/]' for more results. \
        \n'[b]search \[query][/]' for extensive search. \
        \n'[b]sort \[type][/]' for sorting type. (largest, smallest, rating, recent, blank [i][b]= 'sort '[/] for relevance \
        \n'[b]menu[/]' for main menu. \
        \n'[b]exit[/]' to exit.")
        self.select_item_from_results()
 
if __name__ == '__main__':
    os.system("title BetterCinema")
    pretty.install()
    install()
    console = Console()
    os.system('cls' if os.name == 'nt' else 'clear')
    app = Cli()
    app.login()
