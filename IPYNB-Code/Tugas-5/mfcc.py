from library import *
from dataholder import DDIR, types, hop_length, frame_length, scaler

#TODO : Get MFCC and visualize
def get_mfcc(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))
    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13, n_fft=frame_length, hop_length=hop_length)

        librosa.display.specshow(mfcc, x_axis='time', cmap='cool', sr=sr, ax=ax[i])
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_xlabel('Time (s)')
    plt.suptitle(f'MFCC for Audio Number {num:04d}', weight='bold', fontsize=16)
    plt.tight_layout()
    return fig

#TODO : Get Scaled MFCC and visualize
def get_scaled_mfcc(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))
    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')

        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13, n_fft=frame_length, hop_length=hop_length)

        librosa.display.specshow(scale(scaler.fit_transform(mfcc),axis=1), x_axis='time', cmap='cool', sr=sr, ax=ax[i])
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_xlabel('Time (s)')
    plt.suptitle(f'Scaled MFCC for Audio Number {num:04d}', weight='bold', fontsize=16)
    plt.tight_layout()
    return fig