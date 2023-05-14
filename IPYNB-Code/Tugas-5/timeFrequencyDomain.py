from library import *
from dataholder import DDIR, types, hop_length, frame_length, scaler

#TODO : Get Spectogram and visualize
def get_spectogram(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))

    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')

        stft = librosa.stft(y=audio, n_fft=frame_length, hop_length=hop_length)
        mag_spec = np.abs(stft)
        log_spec = librosa.amplitude_to_db(mag_spec)

        librosa.display.specshow(log_spec, sr=sr, x_axis='time', cmap='cool', ax=ax[i])
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_xlabel('Time (s)')
    plt.suptitle(f'Spectogram for Audio Number {num:04d}', weight='bold', fontsize=16)
    plt.tight_layout()
    return fig

#TODO : Mel Spectogram and visualize
def get_mel_spectogram(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5))

    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')

        mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=frame_length, hop_length=hop_length, n_mels=128, fmax=8000)
        log_mel_spec = librosa.power_to_db(mel_spec)

        librosa.display.specshow(log_mel_spec, sr=sr, x_axis='time', cmap='cool', ax=ax[i])
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')
        ax[i].set_xlabel('Time (s)')
    plt.suptitle(f'Mel Spectogram for Audio Number {num:04d}', weight='bold', fontsize=16)
    plt.tight_layout()
    return fig