import requests
import json

class User:
    def __init__(self):
        with open('./config/trakt_config.json') as f:
            self.trakt_config = json.load(f)

    def get(self, type, slug, arg):
        headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': self.trakt_config['application_auth']['client_id']
        }

        if arg:
            request = requests.get(f'https://api.trakt.tv/users/{slug}/{type}/{arg}', headers=headers)
        else:
            request = requests.get(f'https://api.trakt.tv/users/{slug}/{type}', headers=headers)
        return request.json()