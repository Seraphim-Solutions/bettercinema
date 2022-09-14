import requests
import platform
import re

class version_handler:
    def __init__(self):
        self.version = "v1.1.1"
        url = "https://api.github.com/repos/Seraphim-Solutions/bettercinema/releases/latest"
        self.response = requests.get(url).json()
        pass

    def get_version(self):
        latest_tag = self.response['tag_name']
        return latest_tag

    def check_version(self):
        latest_tag = self.response['tag_name']
        if latest_tag == self.version:
            return "You are running the latest version."
        else:
            print(f"Version {latest_tag} available.")
            return self.get_latest_version()

    def get_latest_version(self):
        for assets in self.response['assets']:
            if re.match(f"BetterCinema_{platform.system()}*", assets['name']):
                return f"Direct link: {assets['browser_download_url']}"
            else:
                return f"Sorry, but binary file for {platform.system()} has not been released yet.\nFor more information check latest release: https://github.com/Seraphim-Solutions/bettercinema/releases/tag/v1.1.1"

