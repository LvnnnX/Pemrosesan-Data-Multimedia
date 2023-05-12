#TODO : list of modules
import pandas as pd
import numpy as np
from pathlib import Path
from PIL import Image
import librosa
import librosa.display
import IPython.display as ipd
import matplotlib.pyplot as plt
import seaborn as sns

#TODO : List of directories
BASE = Path(__file__).parent.parent.parent
IMGDIR = BASE / 'Images'
PATH = Path(__file__).parent
DDIR = PATH / 'dataset'
HAPPY = DDIR / 'Happy'
SAD = DDIR / 'Sad'
NEUTRAL = DDIR / 'Neutral'

#TODO :Get my image (Pande Dani Hero Image)
def get_images(name):
    image = Image.open(f'{IMGDIR}/{name}.jpg')
    return image

#TODO: Get allowed num
def get_allowed_number(kelas:str,all_class:list, absen:int) -> list:
    allowed_min = 200 * (all_class.index(kelas)) + (10 * (absen-1)) + 1 #Menghitung nilai minimum yang diizinkan
    allowed_max = allowed_min + 9 #Menghitung nilai maksimum yang diizinkan
    return list(range(allowed_min,allowed_max+1)) #Mengembalikan list dari nilai minimum dan maksimum

#TODO : Get one sample audio and visualize
def get_sample_audio(types:str = ['Happy','Sad','Neutral'], num:int=0):
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))
    audio_list:list = []
    for i,type in enumerate(types):
        audio, sr = librosa.load(f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')
        audio_list.append(audio)
        librosa.display.waveshow(audio, sr=sr, ax=ax[i])
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_ylabel('Amplitude')
        ax[i].set_xlabel('Time (s)')
    plt.tight_layout()
    return audio_list, fig
