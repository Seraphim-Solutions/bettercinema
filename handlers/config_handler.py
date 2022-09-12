import json
import os

class ConfigHandler:
    def __init__(self):
        self.config ={
    "_comment": "you can find all usable colors here https://rich.readthedocs.io/en/stable/appendix/colors.html and styles here https://rich.readthedocs.io/en/stable/style.html, use bold for less eye strain",
    "colors": 
    {
        "bright": {
            "neutral": "white",
            "primary": "blue",
            "info": "turquoise2",
            "good": "green",
            "warning": "yellow",
            "bad": "red"
        },

        "default": {
            "neutral": "bold white",
            "primary": "bold blue",
            "info": "bold turquoise2",
            "good": "bold green",
            "warning": "bold yellow",
            "bad": "bold red"
        }
    },

    "banner":
    {
        "text": "    ___  ____ ___ ___ ____ ____ ____ _ _  _ ____ _  _ ____\n    |__] |___  |   |  |___ |__/ |    | |\\ | |___ |\\/| |__|\n    |__] |___  |   |  |___ |  \\ |___ | | \\| |___ |  | |  |",
        "color": "gold3",
        "animation": 1
    }
}  
        self.trakt_config ={
        "application_auth":
        {    
            "client_id": "804f5a54532dc596711d2534ba689725682e481fcac2b1f70f860f11b689db9c",
            "client_secret": "5b90899d0e7f3b71d98b7c2579b841d99843d1f102b62ae709ddbf4972c84b4f"
        }
    }

        if not os.path.exists('config'):
            os.mkdir('config')
        if not os.path.exists('config/config.json'):
            with open('config/config.json', 'w') as f:
                json.dump(self.config, f)
        if not os.path.exists('config/trakt_config.json'):
            with open('config/trakt_config.json', 'w') as f:
                json.dump(self.trakt_config, f)