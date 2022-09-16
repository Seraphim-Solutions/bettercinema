import json
import requests
from .trakt.oauth import oauth
from .trakt.movies import Movies
from .trakt.shows import Shows
from .trakt.user import User
from .trakt.search import Search


class Trakt:
    """handle trakt api calls"""
    def __init__(self):
        self.oauth = oauth()
        self.Movies = Movies()
        self.Shows = Shows()
        self.User = User()
        self.Search = Search()

    # oauth 
    def authorize_device(self):
        """Authorize device"""
        return self.oauth.authorize_device()

    def get_device_token(self, device_code):
        """Get device token"""
        self.oauth.get_device_token(device_code)

    def get_settings(self):
        """Get settings"""
        self.oauth.get_settings()

    # movies
    def movies(self, arg, limit=""):
        """Get movies"""
        return self.Movies.get(arg, limit)

    # shows
    def shows(self, arg, limit=""):
        """Get shows"""
        return self.Shows.get(arg, limit)


    def seasons(self, arg, season=""):
        """Get seasons for a show"""
        return self.Shows.seasons(arg, season)

    # user
    def user(self, type, slug, arg=None, limit=""):
        """Get user data"""
        return self.User.get(type, slug, arg, limit)

    # search
    def search(self, query, type=""):
        """Search for movies, shows, episodes, people, lists"""
        return self.Search.get(query, type)
