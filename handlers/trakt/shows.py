"""Import modules"""
import json
import requests

from rich.console import Console


class Shows:
    """Handle Trakt shows"""
    def __init__(self):
        """Initialize class"""
        with open('./config/trakt_config.json', encoding="utf-8") as config:
            self.trakt_config = json.load(config)
        self.console = Console()

    def get(self, arg, limit):
        """Get shows from Trakt.tv"""
        with self.console.status(f"Fetching {arg} shows", spinner="dots"):
            headers = {
            'Content-Type': 'application/json',
            'trakt-api-version': '2',
            'trakt-api-key': self.trakt_config['application_auth']['client_id']
            }


            request = requests.get(f'https://api.trakt.tv/shows/{arg}?limit={limit}',
            headers=headers, timeout=350)

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
            request = requests.get(f'https://api.trakt.tv/shows/{arg}/seasons', headers=headers,
            timeout=30)
        else:
            season = "/" + str(season)
            request = requests.get(f'https://api.trakt.tv/shows/{arg}/seasons{season}',
            headers=headers, timeout=30)

        response_body = request.json()
        return response_body
