import requests
import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_handler import db


class oauth:
    def __init__(self):
        self.db = db()
        with open('./config/trakt_config.json') as f:
            self.trakt_config = json.load(f)


    def authorize_device(self):
        cliend_id = self.trakt_config['application_auth']['client_id']

        url = 'https://api.trakt.tv/oauth/device/code'

        payload = {
            'client_id': cliend_id,
        }

        response = requests.post(url, data=payload)
        authorize_data = response.json()
        return [authorize_data['user_code'], authorize_data['verification_url'], authorize_data['device_code']]


    def get_device_token(self, device_code):
        self.current_user = self.db.get_current_user()[0]
        url = 'https://api.trakt.tv/oauth/device/token'

        payload = json.dumps({
            'client_id': self.trakt_config['application_auth']['client_id'],
            'client_secret': self.trakt_config['application_auth']['client_secret'],
            'code': device_code,
        })

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(url, data=payload, headers=headers)
        device_token_data = response.json()
        
        self.db.add_device_auth(device_token_data['access_token'], device_token_data['refresh_token'], device_token_data['expires_in'], device_token_data['created_at'], self.current_user)
    

    def get_settings(self):
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {self.db.read_device_auth()[0][0]}",
        'trakt-api-version': '2',
        'trakt-api-key': self.trakt_config['application_auth']['client_id']
        }


        request = requests.get('https://api.trakt.tv/users/settings', headers=headers)

        response_body = request.json()

        self.db.add_trakt_user_data(response_body['user']['username'], response_body['user']['private'], response_body['user']['vip'], response_body['user']['vip_ep'], response_body['user']['ids']['slug'], self.current_user)
