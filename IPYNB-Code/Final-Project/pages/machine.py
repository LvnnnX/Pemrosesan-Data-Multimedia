from library import *
import UI
from dataholder import get_images

if __name__ == '__main__':
    UI.clear_background()
    UI.make_footer()
    UI.center_image("css-1kyxreq etr89bj2")

    st.markdown("<h1 style='text-align:center; color:white; padding-bottom:5px'>How's Our Machine Works?</h1>", unsafe_allow_html=True)  

    st.markdown("<h2 style='text-align:center; color:white; padding-top:2px;font-weight:bold'>I. Pre-Processing </h2>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:left; color:white; padding-top:40px;font-weight:bold'>a. What function do we use?</h3>", unsafe_allow_html=True)

    st.markdown("Kami menggunakan 3 (tiga) fungsi untuk mengubah data suara menjadi data numerik. Fungsi-fungsi tersebut adalah:")

    st.markdown("<h3 style='padding-left:25px'>1. Root-Mean-Square Energy (RMSE)</h3>", unsafe_allow_html=True)
    st.markdown("Root-Mean-Square Energy (RMSE) adalah fungsi yang digunakan untuk mengukur energi dari sinyal audio. RMSE menghitung nilai rata-rata dari kuadrat dari sinyal audio. RMSE dapat digunakan untuk mengukur kekuatan sinyal audio. Semakin besar nilai RMSE, maka semakin keras sinyal audio tersebut. Sebaliknya, semakin kecil nilai RMSE, maka semakin lemah sinyal audio tersebut.")

    st.code("""def rmse(audio_path:str=None, frame_size:int=2048, hop_len:int=512):
    signal, sr = librosa.load(audio_path)
    rms_energy = librosa.feature.rms(y=signal, frame_length=frame_size, hop_length=hop_len)[0]

    frames = range(0, len(rms_energy))
    times = librosa.frames_to_time(frames, hop_length=hop_len)

    return rms_energy""")

    st.markdown("<h3 style='padding-left:25px'>2. Zero Crossing Rate (ZCR)</h3>", unsafe_allow_html=True)
    st.markdown("Zero-Crossing Rate (ZCR) adalah fungsi yang digunakan untuk mengukur frekuensi dari sinyal audio. ZCR menghitung jumlah perubahan tanda dari sinyal audio. ZCR dapat digunakan untuk mengukur kecepatan sinyal audio. Semakin besar nilai ZCR, maka semakin cepat sinyal audio tersebut. Sebaliknya, semakin kecil nilai ZCR, maka semakin lambat sinyal audio tersebut.")

    st.code("""def zcr(audio_path:str|os.PathLike, frame_size:int=2048, hop_len:int=512):
    signal, sr = librosa.load(audio_path)
    zcr = librosa.feature.zero_crossing_rate(y=signal, frame_length=frame_size, hop_length=hop_len)[0]

    frames = range(0, len(zcr))
    times = librosa.frames_to_time(frames, hop_length=hop_len)

    return zcr""")

    st.markdown("<h3 style='padding-left:25px'>3. Mel-Frequency Cepstral Coefficients (MFCC)</h3>", unsafe_allow_html=True)
    st.markdown("Mel-Frequency Cepstral Coefficients (MFCC) adalah fungsi yang digunakan untuk mengukur frekuensi dari sinyal audio. MFCC menghitung jumlah perubahan tanda dari sinyal audio. MFCC dapat digunakan untuk mengukur kecepatan sinyal audio. Semakin besar nilai MFCC, maka semakin cepat sinyal audio tersebut. Sebaliknya, semakin kecil nilai MFCC, maka semakin lambat sinyal audio tersebut.")

    st.code("""def mfcc(audio_path:str|os.PathLike, frame_rate:int=2048, hop_len:int=512, mfcc_num:int=20):
    signal, sr = librosa.load(audio_path)
    mfcc_spectrum = librosa.feature.mfcc(y=signal, sr=sr, n_fft=frame_rate, hop_length=hop_len, n_mfcc=mfcc_num)
    delta_1_mfcc = librosa.feature.delta(mfcc_spectrum, order=1)
    delta_2_mfcc = librosa.feature.delta(mfcc_spectrum, order=2)

    mfcc_features = np.concatenate((np.mean(mfcc_spectrum, axis=1), np.mean(delta_1_mfcc, axis=1), np.mean(delta_2_mfcc, axis=1)))

    return mfcc_features""")

    st.markdown("<h3 style='text-align:left; color:white; padding-top:40px;font-weight:bold'>b. How do we process the data?</h3>", unsafe_allow_html=True)
    st.markdown('Setelah mendapatkan nilai dari ketiga fungsi tersebut, kami menggabungkan ketiga nilai tersebut menjadi satu data numerik. Data numerik tersebut akan digunakan sebagai input untuk model machine learning yang kami buat.')
    
    st.code("""def get_audio_features(audio_path:str|os.PathLike=DDIR, frame_size:int=2048, hop_len:int=512, mfcc_num:int=20) -> pd.DataFrame:
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
    return df""")

    st.markdown("<h2 style='text-align:center; color:white; padding-top:50px;font-weight:bold'>II. SVM Modeling </h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:left; color:white; padding-top:40px;font-weight:bold'>a. How do we make the model?</h3>", unsafe_allow_html=True)

    st.markdown("Kami menggunakan Support Vector Machine (SVM) sebagai model machine learning yang kami buat. SVM adalah model machine learning yang digunakan untuk melakukan klasifikasi dan regresi. SVM dapat melakukan klasifikasi dengan cara memisahkan data menjadi dua kelas. SVM akan memisahkan data dengan membuat garis atau hiperplane yang memaksimalkan jarak antar kelas. SVM akan memilih garis atau hiperplane yang memiliki margin terbesar. Margin adalah jarak antara garis atau hiperplane dengan data terdekat dari masing-masing kelas. SVM akan memilih garis atau hiperplane yang memiliki margin terbesar karena SVM akan menganggap bahwa garis atau hiperplane tersebut memiliki kemampuan untuk mengklasifikasikan data dengan baik.")

    st.markdown("<h4 style='padding-left:30px'>Ubah skala data numerik</h4>",unsafe_allow_html=True)
    st.code("""from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)""")

    st.markdown('Jangan lupa untuk mengubah skala data numerik yang dimiliki agar data numerik tersebut memiliki skala yang sama. Hal ini dilakukan agar data numerik tersebut dapat diolah dengan baik oleh model machine learning yang kami buat.')

    st.markdown("<h4 style='padding-left:30px'>Membuat model</h4>",unsafe_allow_html=True)
    st.code("""from sklearn.svm import SVC
def svm_train(X_train, X_test, y_train, y_test, kernel:str='linear', C:float=1.0, gamma:str|int=None, dfs:str=None):
    svc = SVC(kernel=kernel, C=C, gamma=gamma, decision_function_shape=dfs, probability=True)
    svc.fit(X_train, y_train)
    y2 = svc.predict(X_test)
    return accuracy_score(y_test, y2)""")

    st.markdown('Setelah data numerik yang kami miliki memiliki skala yang sama, kami membuat model machine learning dengan menggunakan fungsi SVM yang disediakan oleh library scikit-learn. Kami menggunakan fungsi SVM tersebut untuk membuat model machine learning yang dapat melakukan klasifikasi data numerik yang kami miliki.')

    st.markdown("<h3 style='text-align:left; color:white; padding-top:40px;font-weight:bold'>b. How do we get the best model?</h3>", unsafe_allow_html=True)

    st.markdown("Kami menggunakan sebuah fungsi yang memanggil berbagai parameter dan kernel pada algoritma SVM. Fungsi tersebut akan mengembalikan nilai akurasi dari model machine learning yang kami buat. Kami menggunakan fungsi tersebut untuk mencari parameter dan kernel terbaik yang dapat menghasilkan model machine learning dengan akurasi terbaik.")

    st.code("""def get_svm(X_train, X_test, y_train, y_test)->pd.DataFrame:
    df = pd.DataFrame(columns=['kernel', 'C', 'accuracy (%)','gamma','decision_function_shape'])
    list_gamma = [0.0001, 0.001, 0.1, 1, 'auto','scale']
    list_dfs = ['ovo','ovr']
    for a in tqdm(list_dfs):
        for x in [0.1, 1, 10, 100, 1000]:
            for y in ['linear', 'poly', 'rbf', 'sigmoid']:
                for z in list_gamma:
                    acc = svm_train(X_train, X_test, y_train, y_test, y, x, gamma=z, dfs=a)
                    df = df.append({'kernel': y, 'C': x, 'accuracy (%)': acc.round(2), 'gamma': z, 'decision_function_shape':a}, ignore_index=True)
    return df""")

    st.markdown("Keluaran dari fungsi di atas adalah sebagai berikut.")

    st.image(get_images('contoh_output'),width=300)

    st.markdown("<h3 style='text-align:left; color:white; padding-top:40px;font-weight:bold'>c. What the best model?</h3>", unsafe_allow_html=True)

    st.markdown("Setelah mendapatkan nilai akurasi dari berbagai parameter dan kernel pada algoritma SVM, kami memilih parameter dan kernel yang menghasilkan model machine learning dengan akurasi terbaik. Berikut adalah parameter dan kernel yang kami pilih.")
    st.image(get_images('best'), width=300)

    st.markdown("<h2 style='text-align:center; color:white; padding-top:50px;font-weight:bold'>III. Predicting </h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:left; color:white; padding-top:40px;font-weight:bold'>a. How do we predict?</h3>", unsafe_allow_html=True)

    st.markdown("Kami menggunakan model machine learning yang kami buat untuk memprediksi data numerik yang kami miliki. Data numerik tersebut akan kami prediksi menjadi data kelas. Data kelas tersebut akan kami ubah menjadi data sentimen. Data sentimen tersebut akan kami tampilkan kepada pengguna.")

    st.markdown("<h3 style='text-align:left; color:white; padding-top:40px;font-weight:bold'>b. How do we show the result?</h3>", unsafe_allow_html=True)

    st.markdown("Kami menampilkan hasil prediksi data sentimen kepada pengguna dengan menggunakan sebuah fungsi. Fungsi tersebut akan menampilkan data sentimen kepada pengguna dalam bentuk teks dan audio. Fungsi tersebut juga akan menampilkan data numerik yang kami miliki dalam bentuk tabel.")

    st.code("""def get_prediction(model:object=model_1, audio_name:str|None = None, path:os.PathLike|None = None):
    df = get_audio_features(audio_path=f'{path}/{audio_name}')
    X = scaler.transform(df)
    y_pred = model.predict_proba(X)
    return y_pred""")

    