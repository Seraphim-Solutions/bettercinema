import json
import requests

class Search:
    def __init__(self):
        with open('./config/trakt_config.json') as f:
            self.trakt_config = json.load(f)

    def get(self, query, type):
        headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': self.trakt_config['application_auth']['client_id']
        }

        request = requests.get(f'https://api.trakt.tv/search/{type}?query={query}', headers=headers)
        return request.json()