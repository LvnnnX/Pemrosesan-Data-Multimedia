import streamlit as st
import dataholder as dh
import numpy as np
import base64

global sample_rate
sample_rate:int = 22050 #Set sample rate

#TODO : First Function is to get sample audio
def first_run_get_sample():
    st.subheader('Menampilkan sample audio berdasarkan nomor yang anda dapatkan')
    try:
        sample_num:int = int(st.text_input(label='Masukkan Nomor audio untuk sample',placeholder='Ketik Disini!',value=allowed_num[0])) #Input nomor audio
        if(sample_num not in allowed_num):
            raise NameError
    except NameError:
        st.error('Nomor audio harus pada rentang yang anda dapatkan!')
    except Exception as _:
        st.error('Nomor audio harus sebuah angka!')
    else:
        audio,fig=dh.get_sample_audio(num=sample_num)
        st.pyplot(fig)
        col1,col2,col3 = st.columns([1,1,1])
        with col1:
            st.audio(audio[0])
        with col2:
            st.audio(audio[1])
        with col3:
            st.audio(audio[2])
        global num_list
        num_list = get_num_list()
        second_run_time_domain()

#TODO : List 3 number that user want to use (3 each class)
def get_num_list() -> list[int]:
    st.markdown("<h1 style='text-align: center; color:white'>Audio input selection (<font color='red'>3</font> samples)</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: white;'>The default is your 3 first number from allowed numbers</h5>", unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,1,1])
    with col1:
        try:
            num_1:int = (int(st.text_input(label=f'Masukkan Nomor audio untuk sample ke-{1}',placeholder='Ketik Disini!',value=allowed_num[0])))
            if(num_1 not in allowed_num):
                raise NameError
        except NameError:
            st.error('Nomor audio harus pada rentang yang anda dapatkan!')
        except Exception as _:
            st.error('Nomor audio harus sebuah angka!')
    with col2:
        try:
            num_2:int = (int(st.text_input(label=f'Masukkan Nomor audio untuk sample ke-{2}',placeholder='Ketik Disini!',value=allowed_num[0]+1)))
            if(num_2 not in allowed_num):
                    raise NameError
        except NameError:
            st.error('Nomor audio harus pada rentang yang anda dapatkan!')
        except Exception as _:
            st.error('Nomor audio harus sebuah angka!')
    with col3:
        try:
            num_3:int = (int(st.text_input(label=f'Masukkan Nomor audio untuk sample ke-{3}',placeholder='Ketik Disini!',value=allowed_num[0]+2)))
            if(num_3 not in allowed_num):
                    raise NameError
        except NameError:
            st.error('Nomor audio harus pada rentang yang anda dapatkan!')
        except Exception as _:
            st.error('Nomor audio harus sebuah angka!')
    return [num_1,num_2,num_3]


#TODO : Second Function is to show Time-Domain
def second_run_time_domain():

    st.markdown("<h2 style='text-align: center; color: white;'><font color='green'>-==-</font> Time-Domain <font color='green'>-==-</font></h2>", unsafe_allow_html=True)

    #TODO : Amplitude-Time Representation (1/4)
    st.markdown("<h3 style='text-align:center'>Amplitude-Time Representation</h3>\
                <p style='text-align:center'>Menampilkan <font color='grene'>Amplitude-time representation</font> berdasarkan audio yang anda pilih (3 dari 10)</p>", unsafe_allow_html=True)
    #TODO : Amplitude-Time Description
    st.caption(f"Domain waktu atau representasi amplitudo waktu adalah\
                teknik representasi sinyal yang paling dasar,\
                di mana sinyal direpresentasikan sebagai amplitudo yang bervariasi dengan waktu.")

    for num in num_list:
        audio,fig = dh.get_amplitude_time_representation(num)
        st.pyplot(fig)
        col1,col2,col3 = st.columns([1,1,1])
        with col1:
            st.audio(audio[0])
        with col2:
            st.audio(audio[1])
        with col3:
            st.audio(audio[2])


    #TODO : Average Energy (2/4)
    st.markdown("<h3 style='text-align:center'>Average Energy</h3>\
                <p style='text-align:center'>Menampilkan <font color='grene'>Average Energy</font> berdasarkan audio yang anda pilih (3 dari 10)</p>", unsafe_allow_html=True)
    #TODO : Average Energy Description
    st.caption(f"Energi rata-rata menunjukkan kenyaringan sinyal audio.")

    for num in num_list:
        fig = dh.get_average_energy(num)
        st.pyplot(fig)

    #TODO : Zero Crossing Rate (3/4)
    st.markdown("<h3 style='text-align:center'>Zero Crossing Rate</h3>\
                <p style='text-align:center'>Menampilkan <font color='grene'>Zero Crossing Rate</font> berdasarkan audio yang anda pilih (3 dari 10)</p>", unsafe_allow_html=True)
    #TODO : Zero Crossing Rate Description
    st.caption(f"Zero Crossing Rate menunjukkan frekuensi amplitudo sinyal\
    perubahan tanda. Sampai batas tertentu, ini menunjukkan frekuensi sinyal rata-rata.")

    for num in num_list:
        fig = dh.get_zero_crossing_rate(num)
        st.pyplot(fig)

    #TODO : Silence Ratio (4/4)
    st.markdown("<h3 style='text-align:center'>Silence Ratio</h3>\
                <p style='text-align:center'>Menampilkan <font color='grene'>Silence Ratio</font> berdasarkan audio yang anda pilih (3 dari 10)</p>", unsafe_allow_html=True)
    #TODO : Silence Ratio Description
    st.caption(f"Rasio keheningan menunjukkan proporsi bagian suara yang ada\
    diam. Diam didefinisikan sebagai periode di mana nilai-nilai amplitudo mutlak tertentu\
    jumlah sampel berada di bawah ambang batas tertentu. Perhatikan bahwa ada dua ambang batas dalam\
    definisi. Yang pertama digunakan untuk menentukan apakah sampel audio tidak bersuara. Tapi seorang individu diam\
    sampel tidak akan dianggap sebagai periode diam. Hanya bila jumlah sepi berturut-turut\
    sampel di atas ambang waktu tertentu apakah sampel ini dianggap diam\
    periode. Rasio diam dihitung sebagai rasio antara jumlah periode diam dan\
    panjang total bagian audio.\
    Ada beberapa cara untuk mencari :blue[rasio keheningan], namun kasus kali ini developer memilih untuk menetapkan bahwa suara dapat dikatakan :red[hening] jika dan hanya jika amplitudo dari suara tersebut di bawah :red[10%] dari amplitudo maksimum dari suara tersebut.")
    
    for num in num_list:
        silence_rate,fig = dh.get_silence_ratio(num)
        st.pyplot(fig)
        col1,col2,col3 = st.columns([1,1,1])
        with col1:
            st.markdown(f"<p style='text-align:center'>Ratio : {round(silence_rate[0]*100,2)}%</p>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<p style='text-align:center'>Ratio : {round(silence_rate[1]*100,2)}%</p>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<p style='text-align:center'>Ratio : {round(silence_rate[2]*100,2)}%</p>", unsafe_allow_html=True)
    third_run_frequency_domain()


#TODO : Third Function is to show Frequency-Domain
def third_run_frequency_domain():

    st.markdown("<h2 style='text-align: center; color: white;'><font color='green'>-==-</font> Frequency Domain <font color='green'>-==-</font></h2>", unsafe_allow_html=True)

    #TODO : Sound Spectrum Representation (1/3)
    st.markdown("<h3 style='text-align:center'>Sound Spectrum Representation</h3>\
                <p style='text-align:center'>Menampilkan <font color='grene'>Sound Spectrum Representation</font> berdasarkan audio yang anda pilih (3 dari 10)</p>", unsafe_allow_html=True)
    
    #TODO : Sound Spectrum Representation Description
    st.caption(f"Representasi domain waktu tidak menunjukkan frekuensi\
    komponen dan distribusi frekuensi sinyal suara. Ini dapat direpresentasikan dalam\
    domain frekuensi. Representasi domain frekuensi dapat diturunkan dari waktu\
    representasi domain menurut Transformasi Fourier.")

    for num in num_list:
        fig = dh.get_sound_spectrum(num)
        st.pyplot(fig)

    #TODO Bandwidth (2/3)
    st.markdown("<h3 style='text-align:center'>Bandwidth</h3>\
                <p style='text-align:center'>Menampilkan <font color='grene'>Bandwidth</font> berdasarkan audio yang anda pilih (3 dari 10)</p>", unsafe_allow_html=True)

    #TODO : Bandwidth Description
    st.caption(f"Bandwidth menunjukkan rentang frekuensi suara. Musik biasanya\
    memiliki bandwidth yang lebih tinggi daripada sinyal suara. Cara paling sederhana untuk menghitung bandwidth\
    adalah dengan mengambil perbedaan frekuensi antara frekuensi tertinggi dan terendah\
    frekuensi komponen spektrum bukan nol. Dalam beberapa kasus, :red[bukan nol] didefinisikan sebagai di\
    minimal 3 dB di atas tingkat diam.")

    for num in num_list:
        fig = dh.get_bandwidth(num)
        st.pyplot(fig)

    #TODO : Spectral Centroid (3/3)
    st.markdown("<h3 style='text-align:center'>Spectral Centroid</h3>\
                <p style='text-align:center'>Menampilkan <font color='grene'>Spectral Centroid</font> berdasarkan audio yang anda pilih (3 dari 10)</p>", unsafe_allow_html=True)

    #TODO : Spectral Centroid Description
    st.caption(f"Menunjukkan di mana :red[pusat massa] untuk suara berada dan dihitung sebagai rata-rata tertimbang dari frekuensi yang ada dalam suara.")

    for num in num_list:
        fig = dh.get_spectral_centroid(num)
        st.pyplot(fig)

    #TODO : Spectral Roll-Off (Bonus)
    st.markdown("<h3 style='text-align:center'>Spectral Rolloff</h3>\
                <p style='text-align:center'>Menampilkan <font color='grene'>Spectral Rolloff</font> berdasarkan audio yang anda pilih (3 dari 10)</p>", unsafe_allow_html=True)

    #TODO : Spectral Roll-Off Description
    st.caption(f"Menunjukkan frekuensi di mana :red[85%] dari energi spektral berada di bawah frekuensi ini.")

    for num in num_list:
        fig = dh.get_spectral_rolloff(num)
        st.pyplot(fig)


if __name__== '__main__':
    st.markdown("<h2 style='text-align: center; color: white;'>Program Audio Preprocessing</h2>", unsafe_allow_html=True) #Judul Program
    # st.image(dh.get_images('hero'),width=150,caption='Made By Pande Dani, Informatika 2021') #Foto Profile & Nama Developer

    hero_bytes = dh.Path(dh.IMGDIR / 'hero.jpg').read_bytes() #Membaca file gambar
    encoded = base64.b64encode(hero_bytes).decode() #Mengencode file gambar

    st.markdown(f"<img src='data:image/jpg;base64,{encoded}' class='img-fluid' style='width:150px;height:150px;display:block;margin-left:auto;margin-right:auto'>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: white; font-weight:10; font-size:15px'>Made By Pande Dani, Informatika 2021</h3>", unsafe_allow_html=True)

    all_class:list[str] = ['A','B','C','D']
    try:
        get_cls:str = str(st.text_input(label='Masukkan :red[Kelas] Anda!',placeholder='Ketik Disini!',value='B')) #Input kelas
        if(get_cls not in all_class): #Jika kelas yang diinput tidak ada pada list kelas
            raise RuntimeError
        get_num:int = int(st.text_input(label='Masukkan :red[Nomor Absen] Anda!',placeholder='Ketik Disini!',value='5')) #Input nomor absen
        if get_num not in np.arange(1,21): #Jika nomor absen yang diinput tidak ada pada rentang 1 - 20
            raise NameError
    
    except RuntimeError:
        st.error('Kelas hanya boleh A,B,C,D!')
    except NameError:
        st.error('Nomor absen harus diantara 1 - 20!')
    except Exception:
        st.error('Silakan penuhi semua kolom!')

    else:
        global allowed_num #set variabel global
        allowed_num:list[int] = dh.get_allowed_number(get_cls,all_class,get_num) #Mengambil list nomor gambar yang dapat digunakan
        st.write(f'Angka yang dapat anda gunakan adalah',*allowed_num) #Menampilkan list nomor gambar yang dapat digunakan
        first_run_get_sample()
        # third_run_frequency_domain()



#Dibuat oleh Pande Dani
