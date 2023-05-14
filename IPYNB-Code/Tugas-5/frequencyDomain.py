from library import *
from dataholder import DDIR, types, hop_length, frame_length

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