# from textwrap import wrap
import os
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
import platform
import re
from rich import print, pretty
from rich.console import Console
from rich.traceback import install
from rich.table import Table
from InquirerPy import inquirer
from InquirerPy.base.control import Choice


from misc.md5Crypt import md5Crypt
from api.api import BetterCinemaAPI
from handlers.request_parser import Handler
from handlers.vlc_handler import Player
from handlers.infuse_handler import Player_Infuse
from handlers.db_handler import db
from handlers.config_handler import ConfigHandler
from handlers.trakt_handler import Trakt
# from handlers.trakt.oauth import oauth
from handlers.version_handler import VersionHandler
from handlers.connection_handler import ConnectionHandler


class Cli():
    """handles the cli"""
    def __init__(self):
        ConfigHandler()
        with open('config/config.json', 'r', encoding="utf-8") as f:
            self.config = json.load(f)
        self.load_colors()
        self.conn = ConnectionHandler()
        self.test_connection()
        self.bc = BetterCinemaAPI()
        self.rp = Handler()
        self.player = Player()
        self.player_infuse = Player_Infuse()
        self.db = db()
        self.md5crypt = md5Crypt()
        self.trakt = Trakt()
        self.version = VersionHandler()
        self.clear_table_data()
        self.user_logged_in = False
        self.movie_links = []
        self.page = 0
        self.username = ""
        self.user_dict, self.query_dict = {}, {"what": "", "offset": 0, "limit": 25, "category": "video", "sort": ""}
        self.has_trakt_auth = None
        self.update_user_dict()
            
    def update_user_dict(self):
        users = self.db.read_creds()
        if users != []:
            for username, pwhash in users:
                    self.user_dict.update({username: pwhash})
    
    def test_connection(self):
        """Tests the connection"""
        if self.conn.internet() == "BAD":
            print(f"[{self.color_bad}] <ERROR> No internet connection[/]")
            sys.exit()
        if self.conn.webshare() == "BAD":
            print(f"[{self.color_bad}] <ERROR> Can't connect to webshare[/]")
            sys.exit()


    def clear_console(self):
        """Clears the console"""
        os.system('cls' if os.name == 'nt' else 'clear')


    def clear_table_data(self):
        """Clears the table data"""
        self.movie_names, self.movie_idents, self.movie_sizes, self.movie_postive_votes, self.movie_negative_votes = [], [], [], [], []


    def load_colors(self, theme='default'):
        """Loads the colors from the config file"""
        self.color_neutral = self.config['colors'][theme]['neutral']
        self.color_good = self.config['colors'][theme]['good']
        self.color_bad = self.config['colors'][theme]['bad']
        self.color_warning = self.config['colors'][theme]['warning']
        self.color_info = self.config['colors'][theme]['info']
        self.color_primary = self.config['colors'][theme]['primary']
        self.color_banner = self.config['banner']['color']

    def color_theme(self):
        """Changes the color theme"""
        themes = [theme for theme in self.config['colors']]
        options = inquirer.select(message="Color Theme: ", choices=[*themes]).execute()
        
        if options:
            self.load_colors(options)
            self.menu()

    def get_salt(self, username):
        """Gets the salt for the password"""
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
        """Gets the wst token"""
        wst_xml = self.rp.login(username, password)
        xml = ET.fromstring(wst_xml)
        
        if not xml.find('status').text == 'OK':
            print("Invalid credentials.")
            self.login()
            
        self.wst = xml.find('token').text

    def get_password_hash(self, password, salt):
        """Gets the password hash"""
        return hashlib.sha1(self.md5crypt.md5crypt(pw=password, salt=salt).encode('utf-8')).hexdigest()
    

    def stored_account(self):
        """Gets the stored account from the database"""
        user_choice = inquirer.select(message="Choose account: ", choices=[
                *self.user_dict,
                "Add new account",
            ]).execute()

        if user_choice == "Add new account":
            username = inquirer.text(message="Username: ").execute()
            salt = self.get_salt(username)
            password = inquirer.secret(message="Password: ").execute()
            self.get_wst(username, self.get_password_hash(password, salt))
            return username, password
        
        else:
            username = user_choice
            password = self.user_dict[username]
            self.get_wst(username, password)
            return username, password


    def accounts(self):
        self.update_user_dict()
        user_choice = inquirer.select(message="Choose account: ", choices=[
            *self.user_dict,
            "Add new account",
            "Remove account",
            "Back"
        ]).execute()

        if user_choice == "Add new account":
            username = inquirer.text(message="Username: ").execute()
            password = inquirer.secret(message="Password: ").execute()
            salt = self.get_salt(username)
            self.get_wst(username, self.get_password_hash(password, salt))
            self.db.add_creds(username, self.get_password_hash(password, salt))
            self.update_user_dict()
            self.accounts()

        if user_choice == "Remove account":
            user_choice = inquirer.select(message="Choose account: ", choices=[
                *self.user_dict
            ]).execute()
            self.db.remove_creds(user_choice)
            del self.user_dict[user_choice]
            if self.user_dict == {}:
                self.clear_console()
                print("No accounts stored. Please log in.")
                self.login()
            elif len(self.user_dict) == 1:
                self.get_wst(list(self.user_dict.keys())[0], list(self.user_dict.values())[0])
                self.username = list(self.user_dict.keys())[0]
                self.menu()
            else:
                self.accounts()
        
        if user_choice == "Back":
            self.menu()

        else:
            self.get_wst(user_choice, self.user_dict[user_choice])
            self.username = user_choice
            self.menu()

    def login(self):
        """Logs the user into Webshare"""
        if self.db.read_creds() == []:
            username = inquirer.text(message="Username: ").execute()
            password = inquirer.secret(message="Password: ").execute()
            salt = self.get_salt(username)
            self.get_wst(username, self.get_password_hash(password, salt))

        if len(self.user_dict) > 1:
            username, password = self.stored_account()
            self.username = username
            self.clear_console()
            self.menu()

        else:
            username, password = list(self.user_dict.keys())[0], list(self.user_dict.values())[0]
            self.get_wst(username, password)


        if username not in self.user_dict.keys():
            salt = self.get_salt(username)
            self.db.add_creds(username, self.get_password_hash(password, salt))
        
        self.db.get_current_user()
        self.username = username
        self.clear_console()
        self.menu()


    def logout(self):
        """Logs the user out of Webshare"""
        self.db.remove_creds(self.username)
        self.user_logged_in = False
        self.clear_console()
        self.login()


    def search_query(self, query: dict):
        """Searches for soemthing via webshare"""
        self.result_list = self.bc.search(query)
        if self.result_list is None:
            print(f"[{self.color_info}] > No results found[/]\n")
            sleep(2)
            self.menu()


    def menu(self):
        """Shows the main menu"""
        self.clear_table_data()
        self.clear_console()
        new_version = True if self.version.version != self.version.get_version() else False 
        print(f"[{self.color_warning}]New version available: {self.version.get_version()}[/]") if new_version else None
        print(f"[{'blink ' + self.color_banner if self.config['banner']['animation'] == 1 else self.color_banner}]{self.config['banner']['text']}[/]\n          🎬 [i]DanniSec's & Trivarialthea's Project[/] 🎬\n")
        choices = [
            "Default Search",
            "Advanced Search",
            "Open Link",
            Choice("Trakt.tv", "Trakt.tv [Beta]"),
            "Settings",
            "Accounts",
            "Exit"]
        
        choices.insert(-1, "Update") if new_version else None
        search_type = inquirer.select(message="Options: ", choices=choices,
            default="Default Search").execute()
        
        if search_type == "Default Search":
            self.clear_console()
        # seach for movies with self.bc and print movies
            query = inquirer.text(message="Search for: ").execute()
            
            self.query_dict = {"what": query, "offset": 0, "limit": 25, "category": "video", "sort": ""}
            self.search_query(self.query_dict)
            self.list_results(query, sort="")
        
        if search_type == "Advanced Search":
            self.clear_console()
            self.advanced_search()
        
        if search_type == "Open Link":
            self.clear_console()
            link = inquirer.text(message="Link: ").execute()
            self.player.play(link)
            
        if search_type == "Trakt.tv":
            self.clear_console()
            #print("This functionality is not yet implemented.")
            #self.menu()
            self.trakt_auth() if self.has_trakt_auth == None else self.trakt_tv() # temp until trakt handler is implemented | move this to trakt_tv() after trakt handler is implemented
            
        if search_type == "Settings":
            self.clear_console()
            setting = inquirer.select(message="Settings: ", choices=[
                "Color Theme",
                "Check for updates",
                "Back"]).execute()
            if setting == "Color Theme":
                self.color_theme()
            if setting == "Check for updates":
                print(f"[{self.color_neutral}]{self.version.check_version()}[/]")
                input("\nPress enter to go back to the menu...")
                self.menu()
            if setting == "Back":
                self.menu()

        if search_type == "Accounts":
            self.clear_console()
            self.accounts()
        
        if search_type == "Update":
            print(self.version.download_latest_version())
            sys.exit()
        
        if search_type == "Exit":
            sys.exit()

    def advanced_search(self):
        """Shows the advanced search sub-menu"""
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
        self.list_results(query, sort)

    def get_result_data(self):
        """Parses data from the result list"""
        for movie in self.result_list:  
            self.movie_idents.append(movie[0])
            self.movie_names.append(movie[1])
            self.movie_sizes.append(movie[2])
            self.movie_postive_votes.append(movie[3])
            self.movie_negative_votes.append(movie[4])
        return

    def list_results(self, query, sort):
        """Generates table with results"""
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

        print(self.movie_table)
        print(self.help()) 
        self.select_item_from_results()


    def select_item_from_results(self):
        """Selects an item from the results"""
         
        selected_movie = inquirer.text(message="~> ").execute()
        commands = ("help", "more", "search", "sort", "menu", "exit")

        if selected_movie not in commands and selected_movie.isdigit() and \
         int(selected_movie) <= len(self.movie_names):
            selected_movie_index = int(selected_movie) - 1

            movie_name = self.movie_names[selected_movie_index]

            movie_link = self.bc.get_link(ident=self.movie_idents[selected_movie_index],
             wst=self.wst)
            if movie_link == "Error 403":
                print("No link found, maybe the file is password protected.")
                self.select_item_from_results()
            else:
                self.selected_item_options(movie_link, movie_name)

        if selected_movie.lower() == "help":
            print(self.help())
            self.select_item_from_results()

    
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
            self.list_results(self.query_dict["what"], self.query_dict["sort"])

        if "search " in selected_movie:
            self.clear_console()
            self.clear_table_data()
            self.query_dict["what"] = selected_movie.replace("search ", "")
            self.query_dict["offset"] = 0
            self.search_query(self.query_dict)
            self.list_results(self.query_dict["what"], self.query_dict["sort"])

        if selected_movie == "menu":
            self.clear_console()
            self.menu()
        
        if selected_movie == "exit":
            self.clear_console()
            # go back to main menu
            self.menu()
            # close program
            #sys.exit()
        
        else:
            print("Invalid input. Type 'help' for available commands.")
            self.select_item_from_results()
        
        
    def selected_item_options(self, movie_link, movie_name):
        """Shows options for the selected item"""
        choice_list = ["Download", "Get Link", "Play in VLC [Network Stream]"]
        choice_list.append("Play in Infuse") if platform.system() == "Darwin" else None

        item_options = inquirer.select(message="Select item options: ", choices=choice_list).execute()
        
        movie_name = self.sanitize_filename(movie_name)
        # filter the movie_name to remove special characters from the filename
        #movie_name = ''.join(e for e in movie_name if e.isalnum() or e == ' ')

        if item_options == "Download":
            filename = inquirer.text(message="Filename: ", default=movie_name).execute()
            self.rp.download(filename, movie_link)
            self.select_item_from_results()

        if item_options == "Play in VLC [Network Stream]":
            self.player.play(movie_link)
            self.select_item_from_results()

        if item_options == "Play in Infuse":
            self.player_infuse.play(movie_link)
            self.select_item_from_results()

        if item_options == "Get Link":
            print(movie_link)
            self.select_item_from_results()


    def trakt_list_movies(self, query_list):
        """Shows list of movies from trakt.tv"""
        choices = [Choice(self.slug[x], query_list[x]) for x in range(len(self.slug))]
        selection = inquirer.fuzzy(message="Select movie: ", choices=[
                *choices
                ]).execute()
        query = selection.replace("-", ".")
        self.query_dict = {"what": query, "offset": 0, "limit": 25, "category": "video", "sort": ""}
        self.search_query(self.query_dict)
        self.list_results(self.query_dict["what"], self.query_dict["sort"])


    def trakt_tv_movies(self):
        """Shows movies from trakt.tv depending on the selected category"""
        movies_options = inquirer.fuzzy(message="Options: ", choices=[
            Choice("trending", "Trending"),
            Choice("popular", "Popular"),
            Choice("recommended", "Recommended"),
            Choice("watched", "Watched"),
            Choice("collected", "Collected"),
            Choice("anticipated", "Anticipated"),
            Choice("boxoffice", "Box Office"),
            "Search"]).execute()


        if movies_options:
            query_list = []
            if "Search" == movies_options:
                search_query = inquirer.text(message="Search: ").execute()
                movie_list = self.trakt_search_results(search_query, "movie")

            elif "popular" == movies_options:
                movie_list = ([[movie['title'], movie['ids']['slug'], movie['year']] for movie in self.trakt.movies(movies_options, "140000")])

            else:
                movie_list = ([[movie['movie']['title'], movie['movie']['ids']['slug'], movie['movie']['year']] for movie in self.trakt.movies(movies_options, "100000")])
            
            [query_list.append(movie[0]) for movie in movie_list]
            self.slug = [movie[1] for movie in movie_list]
            self.trakt_list_movies(query_list)


    def trakt_episodes(self, episodes):
        """Shows episodes from trakt.tv depending on the selected season"""
        episode_name = [episode['title'] for episode in episodes]
        episode_number = [episode_count for episode_count in range(1, len(episode_name) + 1)]

        choices = [Choice(str(episode_number[i]),
         f"E:{episode_number[i]} {episode_name[i]}") for i in range(len(episode_name))]

        episode = inquirer.fuzzy(message="Select episode: ", choices=choices).execute()
        name = self.selected_slug.replace("-", ".")
        query = f"{name}.S{int(self.season_selection):02d}E{int(episode):02d}"
        self.query_dict = {"what": query, "offset": 0, "limit": 25, "category": "video", "sort": ""}
        self.search_query(self.query_dict)
        self.list_results(self.query_dict["what"], self.query_dict["sort"])


    def trakt_season_list(self, seasons, slug):
        """Shows seasons from trakt.tv depending on the selected show"""
        season_list = [Choice(season, f"Season {season}") for season in seasons]

        self.season_selection = inquirer.fuzzy(message="Select season: ", choices=
        season_list).execute()

        episodes = self.trakt.seasons(slug, self.season_selection)
        self.trakt_episodes(episodes)


    def search_trakt_seasons(self, query_list):
        """Searches for a show's seasons on trakt.tv"""
        choices = [Choice(self.slug[x], query_list[x]) for x in range(len(self.slug))]
        selection = inquirer.fuzzy(message="Select show: ", choices=[
                *choices
                ]).execute()
        seasons = self.trakt.seasons(selection)
        seasons = [season['number'] for season in seasons]
        self.selected_slug = selection
        self.trakt_season_list(seasons, selection)


    def trakt_tv_shows(self):
        """Shows shows from trakt.tv depending on the selected category"""
        shows_options = inquirer.fuzzy(message="Options: ", choices=[
            Choice("trending", "Trending"),
            Choice("popular", "Popular"),
            Choice("recommended", "Recommended"),
            Choice("watched", "Watched"),
            Choice("collected", "Collected"),
            Choice("anticipated", "Anticipated"),
            "Search"]).execute()

        query_list = []
        if shows_options == "Search":
            search_query = inquirer.text(message="Search: ").execute()
            show_list = self.trakt_search_results(search_query, "show")

        elif "popular" == shows_options:
            show_list = ([[show['title'], show['ids']['slug'], show['year']] for show in self.trakt.shows(shows_options, "90000")])

        else:
            show_list = ([[show['show']['title'], show['show']['ids']['slug'], show['show']['year']] for show in self.trakt.shows(shows_options, "90000")])

        [query_list.append(show[0]) for show in show_list]
        self.slug = [show[1] for show in show_list]
            
        self.search_trakt_seasons(query_list)


    def trakt_tv(self):
        """Trak, tv menu"""
        option = inquirer.select(message="Options: ", choices=[
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


    def trakt_list_history_cmd(self):
        """Handle commands in trakt history"""
        options = inquirer.text(message="~> ").execute()
        
        if "search " in options:
            self.clear_console()
            self.clear_table_data()
            self.query_dict["what"] = options.replace("search ", "")
            self.query_dict["offset"] = 0
            self.search_query(self.query_dict)
            self.list_results(self.query_dict["what"], self.query_dict["sort"])

        if options == "menu":
            self.clear_console()
            self.menu()
        
        if options == "exit":
            self.clear_console()
            # close program
            sys.exit()

        else:
            print("Invalid input.\nUsable commands: search, menu, exit")
            self.trakt_list_history_cmd()


    def trakt_list_history(self, history: list):
        """Creates a rich table from history"""
        table = Table(show_header=True, header_style="bold magenta", row_styles=["dim", ""])
        table.add_column("Title", justify="center", no_wrap=True)
        table.add_column("Type", justify="center", no_wrap=True)
        table.add_column("Episode", justify="center", no_wrap=True)
        table.add_column("Date", justify="center", no_wrap=True)

        for item in reversed(history):
            table.add_row(
                f"{item[0]} ({item[1]})",
                item[3],
                "-" if item[4] == "Movie" else f"{item[4]}x{item[5]}",
                item[2]
            )
        print(table)
        self.trakt_list_history_cmd()


    def trakt_user_history(self):
        """Handle user history"""
        history = self.trakt.user("history", self.db.read_trakt_user_data()[0][4], limit=50000)
        history_list = []
        _ = [history_list.append([item['movie']['title'], item['movie']['year'], item['watched_at'],
        item['type'], "Movie"]) if item['type'] == "movie" else history_list.append(
            [item['show']['title'], 
            item['show']['year'], item['watched_at'], item['type'], item['episode']['season'], 
            item['episode']['number']]) for item in history]
        self.trakt_list_history(history_list)

    def trakt_user(self):
        """Shows trakt.tv user options"""
        user_options = inquirer.fuzzy(message="Options: ", choices=[
            Choice("history", "History")]).execute()

        if user_options:
            self.trakt_user_history()


    def trakt_auth(self):
        """Trakt.tv authentication"""
        current_user = self.db.get_current_user()
        if str(current_user) not in str(self.db.read_device_auth()):
            auth_code = self.trakt.authorize_device()
            print(f"Please go to the following URL and enter the code: \
            [bold]{auth_code[0]}[/]\n{auth_code[1]}")

            input("Press enter to continue, after you authorize...")
            self.trakt.get_device_token(auth_code[2])
            self.trakt.get_settings()
            self.trakt_tv()
        else:
            print(f"Already authorized as {self.db.read_trakt_user_data()[0][0]}")
            self.trakt_tv()


    def trakt_search_results(self, search, search_type):
        """Parse results from trakt search"""
        results = self.trakt.search(search, search_type)
        results_list = [[result[search_type]['title'],
        result[search_type]['ids']['slug'], result[search_type]['year']] for result in results]
        return results_list


    def more_results(self):
        """Shows more results"""
        self.page += 25
        self.query_dict['offset'] = self.page
        self.result_list = self.bc.search(self.query_dict)
        self.list_results(self.query_dict["what"], self.query_dict["sort"])

 
    def help(self):
        """Shows available commands and their description when browsing results"""
        help_message = ("Select movie by typing the # (number) of the movie.\n"
         "'[b]more[/]' for more results.\n"
         "'[b]search [query][/]' for extensive search.\n"
         "'[b]sort [type][/]' for sorting type. (largest, smallest, rating, recent, blank [i][b]= 'sort '[/] for relevance\n"
         "'[b]menu[/]' for main menu.\n"
         "'[b]exit[/]' to exit.")

        return help_message
 
 
    def sanitize_filename(self, filename):
        invalid_chars = r'[\/:*?"<>|]'
        sanitized_filename = re.sub(invalid_chars, '', filename)
        return sanitized_filename


if __name__ == '__main__':
    os.system(f"title BetterCinema {VersionHandler().version}")
    pretty.install()
    install()
    console = Console()
    os.system('cls' if os.name == 'nt' else 'clear')
    app = Cli()
    app.login()
