"""Import modules"""
import requests

class ConnectionHandler:
    """Check if user is connected to Internet and if he can connect to Webshare.cz"""
    def __init__(self):
        self.check_internet = "https://google.com"
        self.webshare_url = "https://webshare.cz"


    def internet(self):
        """Check if user is connected to Internet"""
        try:
            response = requests.get(self.check_internet, timeout=5)
            if response.status_code == 200:
                return "OK"

            return "BAD"

        except requests.exceptions.RequestException:
            return "BAD"

    def webshare(self):
        """Check if user can connect to Webshare.cz"""
        try:
            response = requests.get(self.webshare_url, timeout=5)
            if response.status_code == 200:
                return "OK"
            return "BAD"

        except requests.exceptions.RequestException:
            return "BAD"
