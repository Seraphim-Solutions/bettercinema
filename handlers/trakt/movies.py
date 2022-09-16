"""Import modules"""
import json
import requests

from rich.console import Console


class Movies:
    """Handle Trakt movies"""
    def __init__(self):
        with open('./config/trakt_config.json', encoding="utf-8") as f:
            self.trakt_config = json.load(f)
        self.console = Console()

    def get(self, arg, limit):
        """Get movies from Trakt.tv"""
        with self.console.status(f"Fetching {arg} movies", spinner="dots"):
            headers = {
            'Content-Type': 'application/json',
            'trakt-api-version': '2',
            'trakt-api-key': self.trakt_config['application_auth']['client_id']
            }

            request = requests.get(f'https://api.trakt.tv/movies/{arg}?limit={limit}', headers=headers, timeout=350)

            response_body = request.json()
            return response_body
