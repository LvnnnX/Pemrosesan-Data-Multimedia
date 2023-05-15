from library import *
from dataholder import DDIR, types, hop_length, frame_length

#TODO : Amplitude-Time Representation
def get_amplitude_time_representation(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5)) #Membuat figure dan axes
    audio_list:list = [] #Membuat list untuk menyimpan path audio
    for i,type in enumerate(types):
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav') #Membaca audio
        audio_list.append(path) #Menambahkan path audio ke list
        librosa.display.waveshow(audio, sr=sr, ax=ax[i]) #Menampilkan audio 
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold') #Memberi judul
        ax[i].set_ylabel('Amplitude') #Memberi label pada y
        ax[i].set_xlabel('Time (s)') #Memberi label pada x 
    plt.suptitle(f'Amplitude-Time for Audio Number {num:04d}', weight='bold', fontsize=16) #Memberi judul pada figure
    plt.tight_layout() #Mengatur layout
    return audio_list, fig


#TODO : Get audio Average Energy and visualize
def get_average_energy(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5)) #Membuat figure dan axes
    for i,type in enumerate(types): #Looping untuk setiap tipe
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav') #Membaca audio
        rms_energy = librosa.feature.rms(y=audio, frame_length=2048, hop_length=512)[0] #Menghitung RMS Energy

        frames = range(0, len(rms_energy)) #Membuat range untuk frame
        times = librosa.frames_to_time(frames, hop_length=512) #Menghitung times

        librosa.display.waveshow(audio, sr=sr, ax=ax[i]) #Menampilkan audio
        ax[i].plot(times, rms_energy, color='r', label='RMS Energy') #Menampilkan RMS Energy
        ax[i].legend(loc='upper right') #Memberi legend
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold') #Memberi judul
        ax[i].set_ylabel('Amplitude') #Memberi label pada y
        ax[i].set_xlabel('Time (s)') #Memberi label pada x
    plt.suptitle(f'Average Energy for Audio Number {num:04d}', weight='bold', fontsize=16) #Memberi judul pada figure
    plt.tight_layout()
    return fig

#TODO : Get audio Zero Crossing Rate and visualize
def get_zero_crossing_rate(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5)) #Membuat figure dan axes
    for i,type in enumerate(types): #Looping untuk setiap tipe
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav') #Membaca audio
        zero_crossings = librosa.feature.zero_crossing_rate(audio, frame_length=frame_length, hop_length=hop_length)[0] #Menghitung Zero Crossing Rate

        frames = range(0, len(zero_crossings))  #Membuat range untuk frame
        times = librosa.frames_to_time(frames, hop_length=hop_length)   #Menghitung times

        librosa.display.waveshow(audio, ax=ax[i]) #Menampilkan audio
        ax[i].plot(times, zero_crossings, color='r', label='Zero Crossing Rate')    #Menampilkan Zero Crossing Rate
        ax[i].legend(loc='upper right') #Memberi legend
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold') #Memberi judul
        ax[i].set_ylabel('Amplitude')   #Memberi label pada y
        ax[i].set_xlabel('Time (s)')    #Memberi label pada x
    plt.suptitle(f'Zero Crossing Rate for Audio Number {num:04d}', weight='bold', fontsize=16)  #Memberi judul pada figure
    plt.tight_layout()  #Mengatur layout
    return fig

#TODO : Get audio Silence Ratio and visualize
def get_silence_ratio(num:int=0) -> plt.figure:
    fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(15,5)) #Membuat figure dan axes
    silence_rate:list[float] = []   #Membuat list untuk menyimpan silence rate
    for i,type in enumerate(types): #Looping untuk setiap tipe
        audio, sr = librosa.load(path:=f'{DDIR}/{type}/{type.lower()}-{num:04d}.wav')   #Membaca audio
        rms_energy = librosa.feature.rms(y=audio, frame_length=2048, hop_length=512)[0] #Menghitung RMS Energy
        zero_crossings = librosa.feature.zero_crossing_rate(audio, frame_length=frame_length, hop_length=hop_length)[0] #Menghitung Zero Crossing Rate

        silence_rate.append(np.sum(rms_energy < max(rms_energy)*0.1) / float(len(zero_crossings)))  #Menghitung silence rate

        frames = range(0, len(rms_energy))  #Membuat range untuk frame
        times = librosa.frames_to_time(frames, hop_length=512)  #Menghitung times

        librosa.display.waveshow(audio, sr=sr, ax=ax[i])    #Menampilkan audio
        ax[i].plot(times, rms_energy, color='r', label='Silence Rate')  #Menampilkan silence rate
        ax[i].legend(loc='upper right') #Memberi legend
        ax[i].set_title(f'{type.lower()}-{num:04d}.wav',weight='bold')  #Memberi judul
        ax[i].set_ylabel('Amplitude')   #Memberi label pada y
        ax[i].set_xlabel('Time (s)')    #Memberi label pada x
    plt.suptitle(f'Silence Rate for Audio Number {num:04d}', weight='bold', fontsize=16)   #Memberi judul pada figure
    plt.tight_layout()
    return silence_rate,fig