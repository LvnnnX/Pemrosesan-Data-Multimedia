from library import *
from dataholder import DDIR, types, hop_length, frame_length

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