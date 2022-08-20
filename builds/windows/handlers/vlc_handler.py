import os
import platform

import subprocess

class Player():
    def __init__(self):
        self.vlc_path = os.path.join("C:/",  "Program Files", "VideoLAN", "VLC", "vlc.exe")


    def play(self, url):
        if platform.system() == 'Windows':
            subprocess.run([f'{self.vlc_path}', url])
        elif platform.system() == 'Linux':
            os.popen(f'vlc {url} --fullscreen')
        elif platform.system() == 'Darwin':
            os.system(f'/Applications/VLC.app/Contents/MacOS/VLC {url}')
        else:
            print('Not supported')
