import requests

class Handler():
    def __init__(self):
        self.base_url = 'https://webshare.cz/'

    def login(self, username, password_hash):
        url = "https://webshare.cz/api/login/"

        payload={'username_or_email': username,
        'password': password_hash,
        'keep_logged_in': '1'}
        headers = {'X-Requested-With':'XMLHttpRequest','Accept':'text/xml; charset=UTF-8','Referer':self.base_url}

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.content

    def salt(self, username):
        url = "https://webshare.cz/api/salt/"

        payload={'username_or_email': username}
        headers = {'X-Requested-With':'XMLHttpRequest','Accept':'text/xml; charset=UTF-8','Referer':self.base_url}

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.content