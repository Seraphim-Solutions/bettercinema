import requests
import json
from .trakt.oauth import oauth
from .trakt.movies import Movies
from .trakt.shows import Shows
from .trakt.user import User
from .trakt.search import Search

class Trakt:
    def __init__(self):
        self.oauth = oauth()
        self.Movies = Movies()
        self.Shows = Shows()
        self.User = User()
        self.Search = Search()

    # oauth 
    def authorize_device(self):
        return self.oauth.authorize_device()
    
    def get_device_token(self, device_code):
        self.oauth.get_device_token(device_code)
    
    def get_settings(self):
        self.oauth.get_settings()
    
    # movies
    def movies(self, arg):
        return self.movies.get(arg)

    # shows
    def shows(self, arg):
        return self.Shows.get(arg)

    # user
    def user(self, type, slug, arg=None):
        return self.User.get(type, slug, arg)

    # search
    def search(self, query, type=""):
        return self.Search.get(query, type)