import moviepy.editor as mp
import os
import pandas as pd
import numpy as np
import spotipy as sp



def ConvertWav(songname):
    mp3_file = mp.AudioFileClip(songname)
    mp3_file = mp3_file.set_fps(48000)
    songname = songname.strip('.mp3')
    wav_file = songname + '.wav'
    mp3_file.write_audiofile(wav_file)
    

def GetSongs(link):
    os.system(link)    

    p = os.listdir()
    for i in p:
        if not "mp3" in i:
            p.remove(i)

    if '.git' in p:       
        p.remove('.git')
    if 'README.md' in p:
        p.remove('README.md')

    print(p)

    for i in p:
        ConvertWav(i)
        os.remove(i)

#GetSongs(linktoplaylist/songs)