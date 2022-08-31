import requests
import json


class Shows:
    def __init__(self):
        with open('./config/trakt_config.json') as f:
            self.trakt_config = json.load(f)
    
    
    def get(self, arg):
        headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': self.trakt_config['application_auth']['client_id']
        }

        request = requests.get(f'https://api.trakt.tv/shows/{arg}', headers=headers)

        response_body = request.json()
        return response_body