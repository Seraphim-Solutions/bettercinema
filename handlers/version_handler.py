"""Import modules"""
import platform
import re
import requests


class VersionHandler:
    """Handle BetterCinema Version and updates"""
    def __init__(self):
        self.version = "v1.2.0"
        url = "https://api.github.com/repos/Seraphim-Solutions/bettercinema/releases/latest"
        self.response = requests.get(url, timeout=10).json()

    def get_version(self):
        """Get BetterCinema latest version"""
        latest_tag = self.response['tag_name']
        return latest_tag

    def check_version(self):
        """Check BetterCinema version"""
        latest_tag = self.response['tag_name']
        if latest_tag == self.version:
            return "You are running the latest version."
        else:
            print(f"Version {latest_tag} available.")
            return self.get_latest_version()

    def get_latest_version(self):
        """Get BetterCinema latest version"""
        for assets in self.response['assets']:
            if re.match(f"BetterCinema_{platform.system()}*", assets['name']):
                return f"Direct link: {assets['browser_download_url']}"
        return f"Sorry, but binary file for {platform.system()} has not been released yet.\nFor more information check latest release: https://github.com/Seraphim-Solutions/bettercinema/releases/tag/{self.get_version()}"

