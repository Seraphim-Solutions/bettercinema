import json
import os

class ConfigHandler:
    def __init__(self):
        self.config ={
        "_comment": "you can find all usable colors here https://rich.readthedocs.io/en/stable/appendix/colors.html and styles here https://rich.readthedocs.io/en/stable/style.html",
        "colors": {
            "neutral": "bold white",
            "primary": "bold blue",
            "info": "bold light blue",
            "good": "bold green",
            "warning": "bold yellow",
            "bad": "bold red"
        }
    }

        if not os.path.exists('config'):
            os.mkdir('config')
        if not os.path.exists('config/config.json'):
            with open('config/config.json', 'w') as f:
                json.dump(self.config, f)
