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

from sklearn.preprocessing import minmax_scale

#TODO : List of directories
BASE = Path(__file__).parent.parent.parent
IMGDIR = BASE / 'Images'
PATH = Path(__file__).parent
DDIR = PATH / 'dataset'
HAPPY = DDIR / 'Happy'
SAD = DDIR / 'Sad'
NEUTRAL = DDIR / 'Neutral'

global types,hop_length,frame_length
types = ['Happy','Sad','Neutral']
hop_length = 512
frame_length = 2048

#TODO :Get my image (Pande Dani Hero Image)
def get_images(name) -> Image:
    image = Image.open(f'{IMGDIR}/{name}.jpg')
    return image

#TODO: Get allowed num
def get_allowed_number(kelas:str,all_class:list, absen:int) -> list:
    allowed_min:int = 200 * (all_class.index(kelas)) + (10 * (absen-1)) + 1 #Menghitung nilai minimum yang diizinkan
    allowed_max:int = allowed_min + 9 #Menghitung nilai maksimum yang diizinkan
    return list(range(allowed_min,allowed_max+1)) #Mengembalikan list dari nilai minimum dan maksimum

#TODO : Get one sample audio and visualize
def get_sample_audio(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))
    audio_list:list = []
    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')
        audio_list.append(path)
        librosa.display.waveshow(audio, sr=sr, ax=ax[i])
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_ylabel('Amplitude')
        ax[i].set_xlabel('Time (s)')
    plt.suptitle(f'Sample Audio Number {num:04d}', weight='bold', fontsize=16)
    plt.tight_layout()
    return audio_list, fig


#TODO : Amplitude-Time Representation
def get_amplitude_time_representation(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))
    audio_list:list = []
    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')
        audio_list.append(path)
        librosa.display.waveshow(audio, sr=sr, ax=ax[i])
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_ylabel('Amplitude')
        ax[i].set_xlabel('Time (s)')
    plt.suptitle(f'Amplitude-Time for Audio Number {num:04d}', weight='bold', fontsize=16)
    plt.tight_layout()
    return audio_list, fig


#TODO : Get audio Average Energy and visualize
def get_average_energy(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))
    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')
        rms_energy = librosa.feature.rms(y=audio, frame_length=2048, hop_length=512)[0]

        frames = range(0, len(rms_energy))
        times = librosa.frames_to_time(frames, hop_length=512)

        librosa.display.waveshow(audio, sr=sr, ax=ax[i])
        ax[i].plot(times, rms_energy, color='r', label='RMS Energy')
        ax[i].legend(loc='upper right')
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_ylabel('Amplitude')
        ax[i].set_xlabel('Time (s)')
    plt.suptitle(f'Average Energy for Audio Number {num:04d}', weight='bold', fontsize=16)
    plt.tight_layout()
    return fig

#TODO : Get audio Zero Crossing Rate and visualize
def get_zero_crossing_rate(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))
    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')
        zero_crossings = librosa.feature.zero_crossing_rate(audio, frame_length=frame_length, hop_length=hop_length)[0]

        frames = range(0, len(zero_crossings))
        times = librosa.frames_to_time(frames, hop_length=hop_length)

        librosa.display.waveshow(audio, ax=ax[i])
        ax[i].plot(times, zero_crossings, color='r', label='Zero Crossing Rate')
        ax[i].legend(loc='upper right')
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_ylabel('Amplitude')
        ax[i].set_xlabel('Time (s)')
    plt.suptitle(f'Zero Crossing Rate for Audio Number {num:04d}', weight='bold', fontsize=16)
    plt.tight_layout()
    return fig

#TODO : Get audio Silence Ratio and visualize
def get_silence_ratio(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))
    silence_rate:list[float] = []
    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')
        rms_energy = librosa.feature.rms(y=audio, frame_length=2048, hop_length=512)[0]
        zero_crossings = librosa.feature.zero_crossing_rate(audio, frame_length=frame_length, hop_length=hop_length)[0]

        silence_rate.append(np.sum(rms_energy < max(rms_energy)*0.1) / float(len(zero_crossings)))

        frames = range(0, len(rms_energy))
        times = librosa.frames_to_time(frames, hop_length=512)

        librosa.display.waveshow(audio, sr=sr, ax=ax[i])
        ax[i].plot(times, rms_energy, color='r', label='Silence Rate')
        ax[i].legend(loc='upper right')
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_ylabel('Amplitude')
        ax[i].set_xlabel('Time (s)')
    plt.suptitle(f'Silence Rate for Audio Number {num:04d}', weight='bold', fontsize=16)
    plt.tight_layout()
    return silence_rate,fig

#TODO : Get Sound Spectrum and visualize
def get_sound_spectrum(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))
    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')
        stft = np.abs(librosa.stft(audio, n_fft=frame_length, hop_length=hop_length))
        db_value = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

        db_average = np.mean(db_value, axis=1)

        ax[i].plot(db_average, color='r', label='Average Spectrum')
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_xlabel('Frequency (Hz)')
        ax[i].set_ylabel('dB')
        # ax[i].invert_yaxis()
    plt.suptitle(f'Sound Spectrum for Audio Number {num:04d}', weight='bold', fontsize=16)
    plt.tight_layout()
    return fig

#TODO : Get bandwidth and visualize
def get_bandwidth(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))
    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')
        bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr, n_fft=frame_length, hop_length=hop_length, center=True, pad_mode='reflect')[0]

        frames = range(0, len(bandwidth))
        times = librosa.frames_to_time(frames, hop_length=hop_length)

        librosa.display.waveshow(audio, sr=sr, ax=ax[i])
        ax[i].plot(times, minmax_scale(bandwidth, axis=0), color='r', label='Bandwidth')
        ax[i].legend(loc='upper right')
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_ylabel('Amplitude')
        ax[i].set_xlabel('Time (s)')
    plt.suptitle(f'Bandwidth for Audio Number {num:04d}', weight='bold', fontsize=16)
    plt.tight_layout()
    return fig

#TODO : Get Spectral Centroid and visualize
def get_spectral_centroid(num:int=0) -> plt.figure:   
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))
    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')
        spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr, n_fft=frame_length, hop_length=hop_length, center=True, pad_mode='reflect')[0]

        frames = range(0, len(spectral_centroids))
        t = librosa.frames_to_time(frames, hop_length=hop_length)

        librosa.display.waveshow(audio, sr=sr, ax=ax[i])
        ax[i].plot(t, minmax_scale(spectral_centroids, axis=0), color='r', label='Spectral Centroid')
        ax[i].legend(loc='upper right')
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_ylabel('Amplitude')
        ax[i].set_xlabel('Time (s)')
    plt.suptitle(f'Spectral Centroid for Audio Number {num:04d}', weight='bold', fontsize=16)
    plt.tight_layout()
    return fig

#TODO : Get Spectral Rolloff and visualize
def get_spectral_rolloff(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))
    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr, n_fft=frame_length, hop_length=hop_length, center=True, pad_mode='reflect')[0]

        frames = range(0, len(spectral_rolloff))
        t = librosa.frames_to_time(frames, hop_length=hop_length)

        librosa.display.waveshow(audio, sr=sr, ax=ax[i])
        ax[i].plot(t, minmax_scale(spectral_rolloff, axis=0), color='r', label='Spectral Rolloff')
        ax[i].legend(loc='upper right')
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_ylabel('Amplitude')
        ax[i].set_xlabel('Time (s)')
    plt.suptitle(f'Spectral Rolloff for Audio Number {num:04d}', weight='bold', fontsize=16)
    plt.tight_layout()
    return fig