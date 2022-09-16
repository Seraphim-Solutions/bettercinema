import requests
import json


class Shows:
    def __init__(self):
        with open('./config/trakt_config.json') as f:
            self.trakt_config = json.load(f)
    
    
    def get(self, arg, limit):
        """Get shows from Trakt.tv"""
        headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': self.trakt_config['application_auth']['client_id']
        }

        
        request = requests.get(f'https://api.trakt.tv/shows/{arg}?limit={limit}', headers=headers)

        response_body = request.json()
        return response_body
    
    
    def seasons(self, arg, season):
        """Get a list of seasons for a show or episodes in a season."""
        headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': self.trakt_config['application_auth']['client_id']
        }
        if season == "":
            request = requests.get(f'https://api.trakt.tv/shows/{arg}/seasons', headers=headers)
        else:
            season = "/" + str(season)
            request = requests.get(f'https://api.trakt.tv/shows/{arg}/seasons{season}', headers=headers)

        response_body = request.json()
        return response_body