from time import sleep
import os
import platform

class Player_Infuse():
    def __init__(self):
        pass
        
    def play(self, url):
        if platform.system() == 'Darwin':
            os.system(f'open "infuse://x-callback-url/play?url={url}"')
        else:
            print('Not supported')
        

p = Player_Infuse()
