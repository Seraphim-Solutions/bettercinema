"""Import modules"""
import json
import requests

from rich.console import Console


class Search:
    """Handle trakt search"""
    def __init__(self):
        with open('./config/trakt_config.json', encoding="utf-8") as config:
            self.trakt_config = json.load(config)
        self.console = Console()

    def get(self, query, search_type):
        """Handle search request"""
        with self.console.status(f"Searching for {query}", spinner="dots"):
            headers = {
            'Content-Type': 'application/json',
            'trakt-api-version': '2',
            'trakt-api-key': self.trakt_config['application_auth']['client_id']
            }

            request = requests.get(f'https://api.trakt.tv/search/{search_type}?query={query}',
            headers=headers, timeout=30)
            return request.json()
