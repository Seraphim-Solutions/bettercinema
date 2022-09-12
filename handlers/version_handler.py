import requests
import platform

class version_handler:
    def __init__(self):
        self.version = "v1.1.1"
        pass

    def get_version(self):
        url = "https://api.github.com/repos/Seraphim-Solutions/bettercinema/releases/latest"
        response = requests.request("GET", url)

        if response.json()['tag_name'] != self.version:
            for assets in response.json()['assets']:
                if assets['name'] == "BetterCinema_Windows.exe" and platform.system() == "Windows":
                    return "New version available: " + assets['browser_download_url']
                if assets['name'] == "BetterCinema_MacOS" and platform.system() == 'Darwin':
                    return "New version available: " + assets['browser_download_url']
                if assets['name'] == "BetterCinema_Linux" and platform.system() == 'Linux':
                    return "New version available: " + assets['browser_download_url']
                else:
                    return "You are up to date"

print(version_handler().get_version())
