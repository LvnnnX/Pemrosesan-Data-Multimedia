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
        selected_sample_image = st.selectbox( #Box pemilihan untuk memilih mode tampilan dataframe normalize
            label='Select Type',
            options=type,
            key='sample_image'
        )
        sample_image = dataholder.get_sample_image(selected_sample_image.lower(),int(sample_num))
        
        col1,col2,col3 = st.columns([1,2,1])
        with col1:
            st.header('')
        with col2:
            st.image(sample_image,width=300,caption=f'Sample Gambar {selected_sample_image}-{sample_num:04d}.jpg')
        with col3:
            st.header('')
        return second_run_get_pixel_dataframe()

def second_run_get_pixel_dataframe():
    st.subheader('Menampilkan Matrix berdasarkan gambar yang anda pilih')
    try:
        sample_matrix = int(st.text_input(label='Masukkan Nomor Gambar untuk Matrix',placeholder='Ketik Disini!',value=allowed_num[0]))
        if(sample_matrix not in allowed_num):
            raise NameError
    except NameError:
        st.error('Nomor Gambar harus pada rentang yang anda dapatkan!')
    # except Exception:
    #     st.error('Nomor Gambar harus sebuah angka!')
    else:
        selected_sample_matrix = st.selectbox( #Box pemilihan untuk memilih mode tampilan dataframe normalize
            label='Select Type',
            options=type,
            key='sample_matrix'
        )
        sample_matrix_data = dataholder.get_one_matrix(sample_matrix,selected_sample_matrix.lower())
        st.write(sample_matrix_data)
        return third_run_colour_histogram()

def third_run_colour_histogram():
    st.subheader('Menampilkan Histogram berdasarkan gambar yang anda pilih')
    global type_selector_with_all 
    type_selector_with_all = type + ['All']
    try:
        selected_colour_histogram = st.selectbox( #Box pemilihan untuk memilih mode tampilan dataframe normalize
            label='Select Type',
            options=type_selector_with_all,
            key='colour_histogram'
        )
    except Exception:
        st.error('Ada yang salah di mesin nih...')
    else:
        st.pyplot(vis.color_histogram(type=selected_colour_histogram.lower(),num_allowed=allowed_num))
        fourth_run_first_order_statistics()

def fourth_run_first_order_statistics():
    st.subheader('Menampilkan First Order Statistics berdasarkan list gambar')
    try:
        selected_first_order_statistics_type = st.selectbox( #Box pemilihan untuk memilih mode tampilan dataframe normalize
            label='Select Type',
            options=type_selector_with_all,
            key='first_order_statistics'
        )
    except Exception:
        st.error('Ada yang salah di mesin nih...')
    else:
        if(selected_first_order_statistics_type!='All'):
            st.dataframe(dataholder.get_first_order_statistics(type=selected_first_order_statistics_type.lower(),num_allowed=allowed_num))
        else:
            for i in type:
                st.dataframe(dataholder.get_first_order_statistics(type=i.lower(),num_allowed=allowed_num))
        fifth_run_glcm()

def fifth_run_glcm():
    st.subheader('Menampilkan GLCM berdasarkan list gambar')
    try:
        selected_glcm_type = st.selectbox( #Box pemilihan untuk memilih mode tampilan dataframe normalize
            label='Select Type',
            options=type_selector_with_all,
            key='glcm_type_selector'
        )
    except Exception:
        st.error('Ada yang salah di mesin nih...')
    else:
        if(selected_glcm_type!='All'):
            global glcm_dataframe
            glcm_dataframe = glcm.run_glcm(type=selected_glcm_type.lower(),num_allowed=allowed_num)
            st.dataframe(glcm_dataframe)
            sixth_run_texture_histogram()
        else:
            for i in type:
                st.dataframe(glcm.run_glcm(type=i.lower(),num_allowed=allowed_num))
                sixth_run_texture_histogram()

def sixth_run_texture_histogram():
    st.subheader('Menampilkan Texture Histogram berdasarkan list gambar')
    texture_type_selector = ['Dissimilarity','Correlation','Energy','Homogeneity','ASM','IDM','Entropy','All']
    try:
        selected_texture_histogram_type = st.selectbox( #Box pemilihan untuk memilih mode tampilan dataframe normalize
            label='Select Type',
            options=texture_type_selector,
            key='texture_histogram_type_selector'
        )
    except Exception:
        st.error('Ada yang salah di mesin nih...')
    else:
        if(selected_texture_histogram_type!='All'):
            st.pyplot(vis.texture_histogram(type=selected_texture_histogram_type.lower(),df=glcm_dataframe))
        else:
            for i in texture_type_selector[:-1]: 
                st.pyplot(vis.texture_histogram(type=i.lower(),df=glcm_dataframe))


if __name__== '__main__':
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('')
    with col2:
        st.markdown("<h2 style='text-align: center; color: white;'>Program Image Processing</h2>", unsafe_allow_html=True)
        st.image(dataholder.get_images('hero'),width=150,caption='Made By Pande Dani, Informatika 2021') #Foto Profile & Nama Developer
    with col3:
        st.header('')
    all_class = ['A','B','C','D']
    try:
        get_cls = str(st.text_input(label='Masukkan Kelas Anda!',placeholder='Ketik Disini!',value='B'))
        if(get_cls not in all_class):
            raise RuntimeError
        get_num = int(st.text_input(label='Masukkan Nomor Absen',placeholder='Ketik Disini!',value='5'))
        if get_num not in np.arange(1,20):
            raise NameError
    
    except RuntimeError:
        st.error('Kelas hanya boleh A,B,C,D!')
    except NameError:
        st.error('Nomor absen harus diantara 1 - 20!')
    except Exception:
        st.error('Silakan penuhi semua kolom!')

    else:
        global allowed_num
        allowed_num = dataholder.get_allowed_images_num(get_cls,all_class,get_num)
        st.write(f'Angka yang dapat anda gunakan adalah',*allowed_num)
        first_run_get_sample()
#Dibuat oleh Pande Dani