from time import sleep
import os
import platform

class Player():
    def __init__(self):
        pass
        
    def play(self, url):
        if platform.system() == 'Windows':
            os.system(f'start "%PROGRAMFILES%\VideoLAN\VLC\vlc.exe" {url}')
        elif platform.system() == 'Linux':
            os.system(f'vlc {url} --fullscreen')
        elif platform.system() == 'Darwin':
            os.system(f'/Applications/VLC.app/Contents/MacOS/VLC {url}')
        else:
            print('Not supported')
        

p = Player()


