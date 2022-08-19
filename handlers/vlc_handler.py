from time import sleep
import os

class Player():
    def __init__(self):
        pass
        
    def play(self, url):
        os.system(f'vlc {url} --fullscreen')
        

p = Player()


