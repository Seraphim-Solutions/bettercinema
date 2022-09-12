import requests
import platform
import re

class version_handler:
    def __init__(self):
        self.version = "v1.1.1"
        pass

    def get_version(self):
        url = "https://api.github.com/repos/Seraphim-Solutions/bettercinema/releases/latest"
        response = requests.request("GET", url)
        latest_tag = response.json()['tag_name']

        if latest_tag != self.version:
            for assets in response.json()['assets']:
                if re.match(f"BetterCinema_{platform.system()}*", assets['name']):
                    return f"Version {latest_tag} available: {assets['browser_download_url']}"
        else:
            return "You are up to date"