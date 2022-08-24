from re import A
import requests
import json


class oauth:
    def __init__(self):
        with open('./config/trakt_config.json') as f:
            self.trakt_config = json.load(f)

    def authorize_device(self):
        cliend_id = self.trakt_config['application_auth']['client_id']
        client_secret = self.trakt_config['application_auth']['client_secret']

        url = 'https://api.trakt.tv/oauth/device/code'

        payload = {
            'client_id': cliend_id,
        }

        response = requests.post(url, data=payload)
        authorize_data = response.json()
        self.device_code = authorize_data['device_code']

    def get_device_token(self):
        url = 'https://api.trakt.tv/oauth/device/token'

        payload = {
            'client_id': self.trakt_config['application_auth']['client_id'],
            'client_secret': self.trakt_config['application_auth']['client_secret'],
            'code': self.device_code,
        }

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(url, data=payload, headers=headers)
        device_token = response.json()
        self.device_token = device_token['access_token']

