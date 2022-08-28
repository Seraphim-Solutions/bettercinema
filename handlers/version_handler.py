import requests
import platform

class version_handler:
    def __init__(self):
        self.version = "v1.0.0"
        pass

    def get_version(self):
        url = "https://api.github.com/repos/Seraphim-Solutions/bettercinema/releases"
        response = requests.request("GET", url)

        if response.json()[0]['tag_name'] != self.version:
            if platform.system() == 'Linux':
                return "New version available: " + response.json()[0]['assets'][0]['browser_download_url']
            if platform.system() == 'Darwin':
                return "New version available: " + response.json()[0]['assets'][1]['browser_download_url']
            if platform.system() == 'Windows':
                return "New version available: " + response.json()[0]['assets'][2]['browser_download_url']
        else:
            return "You are up to date"

version_handler().get_version()
