"""Import modules"""
import platform
import re
import requests
import sys

class VersionHandler:
    """Handle BetterCinema Version and updates"""
    def __init__(self):
        self.version = "v1.2.4"
        url = "https://api.github.com/repos/Seraphim-Solutions/bettercinema/releases/latest"
        self.response = requests.get(url, timeout=10).json()
        if "message" in self.response:
            sys.tracebacklimit = 0
            raise Exception(self.response["message"])
        
    def get_version(self):
        """Get BetterCinema latest version"""
        latest_tag = self.response['tag_name']
        return latest_tag

    def check_version(self):
        """Check BetterCinema version"""
        if self.get_version == self.version:
            return "You are running the latest version."
        else:
            print(f"Version {self.get_version} available.")
            return self.get_latest_version()

    def get_latest_version(self):
        """Get BetterCinema latest version"""
        for assets in self.response['assets']:
            if re.match(f"BetterCinema_{platform.system()}*", assets['name']):
                return f"Direct link: {assets['browser_download_url']}"
        return f"Sorry, but binary file for {platform.system()} has not been released yet.\nFor more information check latest release: https://github.com/Seraphim-Solutions/bettercinema/releases/tag/{self.get_version()}"


    def download_latest_version(self):
        """Download BetterCinema latest version"""
        os_name = platform.system()
        if os_name == "Windows":
            extension = "exe"
        elif os_name == "Linux":
            extension = "AppImage"
        elif os_name == "Darwin":
            extension = "dmg"

        for assets in self.response['assets']:
            if re.match(f"BetterCinema_{os_name}*", assets['name']):
                url = assets['browser_download_url']
                response = requests.get(url, stream=True)
                with open(f"BetterCinema_{os_name}.{extension}", "wb") as file:
                    for data in response.iter_content(chunk_size=1024):
                        file.write(data)
                return f"Downloaded: BetterCinema_{os_name}.{extension}"
        return f"Sorry, but binary file for {os_name} has not been released yet.\nFor more information check latest release: https://github.com/Seraphim-Solutions/bettercinema/releases/tag/{self.get_version()}"