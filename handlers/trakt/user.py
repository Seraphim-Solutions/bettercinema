"""Import modules"""
import json
import requests

from rich.console import Console

class User:
    """Handle Trakt user"""
    def __init__(self):
        with open('./config/trakt_config.json', encoding="utf-8") as config:
            self.trakt_config = json.load(config)
        self.console = Console()

    def get(self, type, slug, arg, limit):
        """Handle user request"""
        with self.console.status(f"Fetching {type}", spinner="dots"):
            headers = {
            'Content-Type': 'application/json',
            'trakt-api-version': '2',
            'trakt-api-key': self.trakt_config['application_auth']['client_id']
            }

            if arg:
                request = requests.get(f'https://api.trakt.tv/users/{slug}/{type}/{arg}?limit={limit}', headers=headers, timeout=350)
            else:
                request = requests.get(f'https://api.trakt.tv/users/{slug}/{type}?limit={limit}', headers=headers, timeout=350)
            return request.json()