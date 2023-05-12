import streamlit as st
import dataholder as dh
import numpy as np

global sample_rate
sample_rate:int = 22050 #Set sample rate

#TODO : First Function is to get sample audio
def first_run_get_sample():
    st.subheader('Menampilkan Sample Gambar berdasarkan nomor yang anda dapatkan')
    try:
        sample_num:int = int(st.text_input(label='Masukkan Nomor Gambar untuk sample',placeholder='Ketik Disini!',value=allowed_num[0])) #Input nomor gambar
        if(sample_num not in allowed_num):
            raise NameError
    except NameError:
        st.error('Nomor Gambar harus pada rentang yang anda dapatkan!')
    except Exception:
        st.error('Nomor Gambar harus sebuah angka!')
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









if __name__== '__main__':
    col1,col2,col3 = st.columns(3) #Membuat kolom
    with col1:
        st.header('')
    with col2:
        st.markdown("<h2 style='text-align: center; color: white;'>Program Audio Preprocessing</h2>", unsafe_allow_html=True) #Judul Program
        st.image(dh.get_images('hero'),width=150,caption='Made By Pande Dani, Informatika 2021') #Foto Profile & Nama Developer
    with col3:
        st.header('')
    all_class:list[str] = ['A','B','C','D']
    try:
        get_cls:str = str(st.text_input(label='Masukkan Kelas Anda!',placeholder='Ketik Disini!',value='B')) #Input kelas
        if(get_cls not in all_class): #Jika kelas yang diinput tidak ada pada list kelas
            raise RuntimeError
        get_num:int = int(st.text_input(label='Masukkan Nomor Absen',placeholder='Ketik Disini!',value='5')) #Input nomor absen
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



#Dibuat oleh Pande Dani
