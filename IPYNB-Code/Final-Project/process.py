from library import *
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pickle

model_1 = pickle.load(open(PATH / 'svm_model_kelompok_dimas_pande_wahyu.pkl', 'rb'))
# model_2 = pickle.load(open(PATH / 'cnn_model_kelompok_dimas_pande_wahyu.pkl', 'rb'))

# scaler = joblib.load(PATH / 'svm_scaler_kelompok_dimas_pande_wahyu.joblib')

scaler = pickle.load(open(PATH / 'svm_scaler_kelompok_dimas_pande_wahyu.pkl', 'rb'))

# def show_saveshow(name:str= None, directory:os.PathLike = TMPDIR):
#     audio_obj = ipd.Audio(f'{directory}/{name}')
#     audio, sr = librosa.load(f'{directory}/{name}')

#     fig, ax = plt.subplots(figsize=(10,5))

#     ax = librosa.display.waveshow(audio, sr=sr)
#     fig.suptitle(f'Waveplot {name}', fontsize=16)
#     plt.xlabel('Time (s)')
#     plt.ylabel('Amplitude')

#     return fig

def mfcc(signal, frame_rate:int=2048, hop_len:int=512, mfcc_num:int=20, sr:int=None):
    # signal, sr = librosa.load(audio_path, sr=16000)
    mfcc_spectrum = librosa.feature.mfcc(y=signal, sr=sr, n_fft=frame_rate, hop_length=hop_len, n_mfcc=mfcc_num)
    delta_1_mfcc = librosa.feature.delta(mfcc_spectrum, order=1)
    delta_2_mfcc = librosa.feature.delta(mfcc_spectrum, order=2)

    mfcc_features = np.concatenate((np.mean(mfcc_spectrum, axis=1), np.mean(delta_1_mfcc, axis=1), np.mean(delta_2_mfcc, axis=1)))

    return mfcc_features

def zcr(signal, frame_size:int=2048, hop_len:int=512):
    # signal, sr = librosa.load(audio_path, sr=16000)
    zcr = librosa.feature.zero_crossing_rate(y=signal, frame_length=frame_size, hop_length=hop_len)[0]

    frames = range(0, len(zcr))
    times = librosa.frames_to_time(frames, hop_length=hop_len)

    return zcr

def rmse(signal, frame_size:int=2048, hop_len:int=512):
    # signal, sr = librosa.load(audio_path, sr=16000)
    rms_energy = librosa.feature.rms(y=signal, frame_length=frame_size, hop_length=hop_len)[0]

    frames = range(0, len(rms_energy))
    times = librosa.frames_to_time(frames, hop_length=hop_len)

    return rms_energy

def get_audio_features(audio_path, frame_size:int=2048, hop_len:int=512, mfcc_num:int=20) -> pd.DataFrame:
    audios_mfcc, audios_zcr, audios_rmse = [],[],[]

    audio, sr = librosa.load(audio_path)

    mfcc_score = mfcc(audio, frame_rate=frame_size, hop_len=hop_len, mfcc_num=mfcc_num, sr=sr)

    zcr_score = np.mean(zcr(audio, frame_size=frame_size, hop_len=hop_len))

    rmse_score = np.mean(rmse(audio, frame_size=frame_size, hop_len=hop_len))

    audios_mfcc.append(mfcc_score)
    audios_zcr.append(zcr_score)
    audios_rmse.append(rmse_score)
    # audios_label.append(audio_path.split('/')[-1].split('.')[0])

    audio_features = np.column_stack((audios_mfcc, audios_zcr, audios_rmse))
    df = pd.DataFrame(audio_features)
    return df

def get_prediction(audio_name, model=model_1):
    df = get_audio_features(audio_path=audio_name)
    X = scaler.transform(df)
    y_pred = model.predict_proba(X)
    return y_pred
    