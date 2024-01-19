import requests
import urllib
import os 
from tqdm import tqdm


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
    
    def download(self, filename, url):
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        response = requests.get(url, stream=True)

        total_size_in_bytes = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

        with open(f'downloads/{filename}', 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")