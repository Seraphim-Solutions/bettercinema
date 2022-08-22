import requests
import urllib
import os 
import trakt.core

from trakt import init
from trakt import movies
from trakt.movies import Movie
from trakt.movies import get_recommended_movies

class Handler:
    def __init__(self):
        self.my_client_id = '804f5a54532dc596711d2534ba689725682e481fcac2b1f70f860f11b689db9c'
        self.my_client_secret = '5b90899d0e7f3b71d98b7c2579b841d99843d1f102b62ae709ddbf4972c84b4f'
        trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH

    def login(self, username='SkyCityCZ'):
        init(username, client_id=self.my_client_id, client_secret=self.my_client_secret, store=True)
        print("Login done")
        

    def getRecommendedMovies():
        return get_recommended_movies()

    def getPopularMovies():
        return movies.trending_movies

    def markMovieAsSeen(movie):
        Movie(movie).mark_as_seen()

Handler().getPopularMovies()