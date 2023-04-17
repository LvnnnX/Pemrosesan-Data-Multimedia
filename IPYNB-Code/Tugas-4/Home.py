import streamlit as st
import dataholder
import visualization as vis
import glcm
import numpy as np

def first_run_get_sample():
    st.subheader('Menampilkan Sample Gambar berdasarkan nomor yang anda dapatkan')
    try:
        sample_num = int(st.text_input(label='Masukkan Nomor Gambar untuk sample',placeholder='Ketik Disini!',value=allowed_num[0])) #Input nomor gambar
        if(sample_num not in allowed_num):
            raise NameError
    except NameError:
        st.error('Nomor Gambar harus pada rentang yang anda dapatkan!')
    except Exception:
        st.error('Nomor Gambar harus sebuah angka!')
    else:
        global type
        type = ['Happy','Sad','Neutral']
        selected_sample_image = st.selectbox( #Box pemilihan untuk sample gambar
            label='Select Type',
            options=type,
            key='sample_image'
        )
        sample_image = dataholder.get_sample_image(selected_sample_image.lower(),int(sample_num))
        
        col1,col2,col3 = st.columns([1,2,1])
        with col1:
            st.header('')
        with col2:
            st.image(sample_image,width=300,caption=f'Sample Gambar {selected_sample_image}-{sample_num:04d}.jpg') #Menampilkan gambar
        with col3:
            st.header('')
        second_run_get_pixel_dataframe()

def second_run_get_pixel_dataframe():
    st.subheader('Menampilkan Matrix berdasarkan gambar yang anda pilih')
    try:
        sample_matrix = int(st.text_input(label='Masukkan Nomor Gambar untuk Matrix',placeholder='Ketik Disini!',value=allowed_num[0])) #Input nomor gambar untuk matrix
        if(sample_matrix not in allowed_num): #Jika nomor gambar tidak ada pada rentang yang diberikan
            raise NameError #Maka akan muncul error (NameError)
    except NameError: #Jika terjadi error
        st.error('Nomor Gambar harus pada rentang yang anda dapatkan!')
    except Exception:
        st.error('Nomor Gambar harus sebuah angka!')
    else:
        selected_sample_matrix = st.selectbox( #Box pemilihan sample matrix
            label='Select Type',
            options=type,
            key='sample_matrix'
        )
        sample_matrix_data = dataholder.get_one_matrix(sample_matrix,selected_sample_matrix.lower()) #Mengambil matrix dari dataholder
        st.write(sample_matrix_data) #Menampilkan matrix
        third_run_colour_histogram() #Menjalankan fungsi untuk menampilkan histogram

def third_run_colour_histogram(): #Fungsi untuk menampilkan histogram
    st.subheader('Menampilkan Histogram berdasarkan gambar yang anda pilih')
    global type_selector_with_all #set variabel global
    type_selector_with_all = type + ['All'] #Menambahkan 'All' pada list type
    try:
        selected_colour_histogram = st.selectbox( #Box pemilihan untuk memilih mode tampilan histogram
            label='Select Type',
            options=type_selector_with_all,
            key='colour_histogram'
        )
    except Exception:
        st.error('Ada yang salah di mesin nih...')
    else:
        st.pyplot(vis.color_histogram(type=selected_colour_histogram.lower(),num_allowed=allowed_num)) #Menampilkan histogram
        fourth_run_first_order_statistics() #Menjalankan fungsi untuk menampilkan first order statistics

def fourth_run_first_order_statistics(): #Fungsi untuk menampilkan first order statistics
    st.subheader('Menampilkan First Order Statistics berdasarkan list gambar')
    try:
        selected_first_order_statistics_type = st.selectbox( #Box pemilihan dataframe First Order Statistics berdasarkan tipe gambar
            label='Select Type',
            options=type_selector_with_all,
            key='first_order_statistics'
        )
    except Exception:
        st.error('Ada yang salah di mesin nih...')
    else:
        if(selected_first_order_statistics_type!='All'): #Jika tipe gambar yang dipilih bukan 'All' 
            st.dataframe(dataholder.get_first_order_statistics(type=selected_first_order_statistics_type.lower(),num_allowed=allowed_num)) #Maka akan menampilkan dataframe first order statistics berdasarkan tipe gambar yang dipilih
        else:
            for i in type: 
                st.dataframe(dataholder.get_first_order_statistics(type=i.lower(),num_allowed=allowed_num)) #Tampilkan dataframe first order statistics berdasarkan tipe gambar yang dipilih, jika tipe gambar yang dipilih adalah 'All'
        fifth_matrix_glcm() #Menjalankan fungsi untuk menampilkan matrix glcm

def fifth_matrix_glcm():
    st.subheader('Menampilkan Matrix GLCM berdasarkan list gambar')
    try:
        selected_glcm_type = st.selectbox( #Box pemilihan untuk tipe gambar saat sample matrix
            label='Select Type',
            options=type,
            key='matrix_glcm_selector'
        )
        glcm_matrix_no = int(st.text_input(label='Masukkan Nomor Gambar untuk GLCM Matrix',placeholder='Ketik Disini!',value=allowed_num[0])) #Input nomor gambar untuk matrix
        if(glcm_matrix_no not in allowed_num): #Jika nomor gambar tidak ada pada rentang yang diberikan
            raise NameError #Maka akan muncul error (NameError)
    except NameError: #Jika terjadi error
        st.error('Nomor Gambar harus pada rentang yang anda dapatkan!')
    except Exception:
        st.error('Input harus sebuah angka!')
    else:
        get_image = dataholder.get_sample_image(type=selected_glcm_type.lower(),num=glcm_matrix_no) #Mengambil gambar dari dataholder
        st.write(glcm.get_glcm(get_image),width=300) #Menampilkan matrix glcm
        sixth_run_glcm() #Menjalankan fungsi untuk menampilkan dataframe glcm

def sixth_run_glcm(): #Fungsi untuk menampilkan dataframe glcm
    st.subheader('Menampilkan Data GLCM berdasarkan list gambar')
    try:
        selected_glcm_type = st.selectbox( #Box pemilihan untuk tipe gambar untuk dataframe GLCM
            label='Select Type',
            options=type_selector_with_all,
            key='glcm_type_selector'
        )
    except Exception:
        st.error('Ada yang salah di mesin nih...')
    else:
        global glcm_dataframe #set variabel global
        if(selected_glcm_type!='All'): #Jika tipe gambar yang dipilih bukan 'All'
            glcm_dataframe = glcm.run_glcm(type=selected_glcm_type.lower(),num_allowed=allowed_num) #Maka akan menampilkan dataframe glcm berdasarkan tipe gambar yang dipilih
            st.dataframe(glcm_dataframe) #Menampilkan dataframe glcm
        else:
            for i in type: #Jika tipe gambar yang dipilih adalah 'All'
                glcm_dataframe = glcm.run_glcm(type=i.lower(),num_allowed=allowed_num) #Maka akan menampilkan dataframe glcm berdasarkan tipe gambar yang dipilih
                st.dataframe(glcm_dataframe) #Menampilkan dataframe glcm
        seventh_run_texture_histogram() #Menjalankan fungsi untuk menampilkan texture histogram

def seventh_run_texture_histogram(): #Fungsi untuk menampilkan texture histogram
    st.subheader('Menampilkan Texture Histogram berdasarkan list gambar') #Menampilkan subheader
    texture_type_selector = ['Dissimilarity','Correlation','Energy','Homogeneity','ASM','IDM','Entropy','All'] #List tipe texture histogram
    try:
        selected_texture_histogram_type = st.selectbox( #Box pemilihan untuk memilih tipe/kolom dari texture histogram
            label='Select Type',
            options=texture_type_selector,
            key='texture_histogram_type_selector'
        )
    except Exception:
        st.error('Ada yang salah di mesin nih...')
    else:
        if(selected_texture_histogram_type!='All'): #Jika tipe texture histogram yang dipilih bukan 'All'
            st.pyplot(vis.texture_histogram(type=selected_texture_histogram_type.lower(),df=glcm_dataframe)) #Maka akan menampilkan texture histogram berdasarkan tipe texture histogram yang dipilih
        else:
            for i in texture_type_selector[:-1]: #Jika tipe texture histogram yang dipilih adalah 'All'
                st.pyplot(vis.texture_histogram(type=i.lower(),df=glcm_dataframe)) #Maka akan menampilkan texture histogram berdasarkan tipe texture histogram yang dipilih


if __name__== '__main__':
    col1,col2,col3 = st.columns(3) #Membuat kolom
    with col1:
        st.header('')
    with col2:
        st.markdown("<h2 style='text-align: center; color: white;'>Program Image Processing</h2>", unsafe_allow_html=True) #Judul Program
        st.image(dataholder.get_images('hero'),width=150,caption='Made By Pande Dani, Informatika 2021') #Foto Profile & Nama Developer
    with col3:
        st.header('')
    all_class = ['A','B','C','D']
    try:
        get_cls = str(st.text_input(label='Masukkan Kelas Anda!',placeholder='Ketik Disini!',value='B')) #Input kelas
        if(get_cls not in all_class): #Jika kelas yang diinput tidak ada pada list kelas
            raise RuntimeError
        get_num = int(st.text_input(label='Masukkan Nomor Absen',placeholder='Ketik Disini!',value='5')) #Input nomor absen
        if get_num not in np.arange(1,20): #Jika nomor absen yang diinput tidak ada pada rentang 1 - 20
            raise NameError
    
    except RuntimeError:
        st.error('Kelas hanya boleh A,B,C,D!')
    except NameError:
        st.error('Nomor absen harus diantara 1 - 20!')
    except Exception:
        st.error('Silakan penuhi semua kolom!')

    else:
        global allowed_num #set variabel global
        allowed_num = dataholder.get_allowed_images_num(get_cls,all_class,get_num) #Mengambil list nomor gambar yang dapat digunakan
        st.write(f'Angka yang dapat anda gunakan adalah',*allowed_num) #Menampilkan list nomor gambar yang dapat digunakan
        first_run_get_sample() #Menjalankan fungsi untuk menampilkan sample gambar
#Dibuat oleh Pande Dani