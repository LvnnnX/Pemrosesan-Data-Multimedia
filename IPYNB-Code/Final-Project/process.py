from library import *
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pickle

model_1 = pickle.load(open(PATH / 'svm_model_kelompok_dimas_pande_wahyu.pkl', 'rb'))

scaler = joblib.load(PATH / 'svm_scaler_kelompok_dimas_pande_wahyu.joblib')

# def show_saveshow(name:str= None, directory:os.PathLike = TMPDIR):
#     audio_obj = ipd.Audio(f'{directory}/{name}')
#     audio, sr = librosa.load(f'{directory}/{name}')

#     fig, ax = plt.subplots(figsize=(10,5))

#     ax = librosa.display.waveshow(audio, sr=sr)
#     fig.suptitle(f'Waveplot {name}', fontsize=16)
#     plt.xlabel('Time (s)')
#     plt.ylabel('Amplitude')

#     return fig

def mfcc(audio_path:str|os.PathLike, frame_rate:int=2048, hop_len:int=512, mfcc_num:int=20):
    signal, sr = librosa.load(audio_path)
    mfcc_spectrum = librosa.feature.mfcc(y=signal, sr=sr, n_fft=frame_rate, hop_length=hop_len, n_mfcc=mfcc_num)
    delta_1_mfcc = librosa.feature.delta(mfcc_spectrum, order=1)
    delta_2_mfcc = librosa.feature.delta(mfcc_spectrum, order=2)

    mfcc_features = np.concatenate((np.mean(mfcc_spectrum, axis=1), np.mean(delta_1_mfcc, axis=1), np.mean(delta_2_mfcc, axis=1)))

    return mfcc_features

def zcr(audio_path:str|os.PathLike, frame_size:int=2048, hop_len:int=512):
    signal, sr = librosa.load(audio_path)
    zcr = librosa.feature.zero_crossing_rate(y=signal, frame_length=frame_size, hop_length=hop_len)[0]

    frames = range(0, len(zcr))
    times = librosa.frames_to_time(frames, hop_length=hop_len)

    return zcr

def rmse(audio_path:str=None, frame_size:int=2048, hop_len:int=512):
    signal, sr = librosa.load(audio_path)
    rms_energy = librosa.feature.rms(y=signal, frame_length=frame_size, hop_length=hop_len)[0]

    frames = range(0, len(rms_energy))
    times = librosa.frames_to_time(frames, hop_length=hop_len)

    return rms_energy

def get_audio_features(audio_path:str|os.PathLike=DDIR, frame_size:int=2048, hop_len:int=512, mfcc_num:int=20) -> pd.DataFrame:
    audios_mfcc, audios_zcr, audios_rmse, audios_label = [],[],[],[]

    mfcc_score = mfcc(audio_path=f'{audio_path}', frame_rate=frame_size, hop_len=hop_len, mfcc_num=mfcc_num)

    zcr_score = np.mean(zcr(audio_path=f'{audio_path}', frame_size=frame_size, hop_len=hop_len))

    rmse_score = np.mean(rmse(audio_path=f'{audio_path}', frame_size=frame_size, hop_len=hop_len))

    audios_mfcc.append(mfcc_score)
    audios_zcr.append(zcr_score)
    audios_rmse.append(rmse_score)
    audios_label.append(audio_path.split('/')[-1].split('.')[0])

    audio_features = np.column_stack((audios_mfcc, audios_zcr, audios_rmse))
    df = pd.DataFrame(audio_features)
    return df

def get_prediction(model:object=model_1, audio_name:str|None = None, path:os.PathLike|None = None):
    df = get_audio_features(audio_path=f'{path}/{audio_name}')
    X = scaler.transform(df)
    y_pred = model.predict_proba(X)
    return y_pred
    