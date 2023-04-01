import streamlit as st
import dataholder
import convert
import stopstem
import change_text
import pandas as pd

def get_progress():
    try:
        data = dataholder.get_sample(dataholder.df,get_num) #Memanggil get_sample pada dataholder, untuk memilih 10 baris ulasan pada dataset
        st.write('##')
        st.subheader('Sample Data')
        st.dataframe(data=data.head(),width=1000*len(data.columns)) #Meanmpilkan hasil get_sample, yaitu 10 baris ulasan sesuai ketentuan soal

################################################################################################################################################################################
        st.write("##")
        st.subheader('Drop No Column')
        st.write(f'Karena kolom \'No\' tidak memiliki pengaruh terhadap data (residual) maka kita drop kolom \'No\'')
        data = dataholder.drop_column(data,['No']) #Memanggil drop_column pada dataholder, untuk membuang kolom 'No'
        st.dataframe(data=data.head(),width=1000*len(data.columns)) #Menampilkan hasil setelah membuang kolom 'No'
################################################################################################################################################################################

################################################################################################################################################################################
        st.write('##')
        st.header(f'Preprocessing')
################################################################################################################################################################################

################################################################################################################################################################################
        st.subheader(f'Tokenizing (menghilangkan whitespaces)')
        data_token = convert.tokenize(data['Reviews'])
        st.dataframe(data=data_token, width=1000)
        st.write(f'Panjang data token : {data_token.shape[0]}')
################################################################################################################################################################################


################################################################################################################################################################################
        st.subheader(f'Lowercasing')
        st.write(f'Mengubah text menjadi lowercase menggunakan .lower()')
        st.code(".str.lower()")
        data['Clean'] = convert.make_lower(data.Reviews) #Memanggil make_lower pada convert, untuk menkonversi teks untuk menjadi huruf kecil
        data = convert.change_column(data) #Memanggil change_colum pada convert, untuk memindahkan kolom label yang ada ditengah-tengah antara Reviews dan Clean
        data_token['Words'] = convert.make_lower(data_token['Words'])

        select_type_dataframe = ['Token Only', 'With Raw Data']

        selected_lower = st.selectbox( #Box pemilihan untuk memilih dataframe
            label='Select Dataframe Type',
            options=select_type_dataframe,
            key='selectlower'
        )
        if(selected_lower == select_type_dataframe[0]):
            st.dataframe(data=data_token, width=1000)
        else:
            st.dataframe(data=data.head(),width=1000*len(data.columns)) #Menampilkan hasil setelah lowercasing dan pemindahan kolom
################################################################################################################################################################################


################################################################################################################################################################################
        # st.write('##')
        st.subheader(f'Removing Digits')
        st.write(f'Menghilangkan digit pada text menggunakan .replace()')
        st.code(".str.replace('\d+','')")
        data_token['Words'] = convert.remove_digit(data_token.Words)
        data_token = dataholder.remove_empty(data_token)
        data.Clean = convert.remove_digit(data.Clean) #Memanggil remove_digit pada convert, untuk menghilangkan digit (angka) pada teks
        selected_digit = st.selectbox( #Box pemilihan untuk memilih mode tampilan dataframe remove digits
            label='Select Dataframe Type',
            options=select_type_dataframe,
            key='selectdigit'
        )
        if(selected_digit == select_type_dataframe[0]):
            st.dataframe(data=data_token, width=1000)
            st.write(f'Panjang data token menjadi : {data_token.shape[0]}')
        else:
            st.dataframe(data=data.head(),width=1000*len(data.columns)) #Menampilkan hasil setelah digit dihilangkan
################################################################################################################################################################################


################################################################################################################################################################################
        st.subheader(f'Removing Punctuation')
        st.write(f'Menghilangkan tanda baca, tautan (links), dan whitespaces menggunakan .translate().strip()')
        st.code(".str.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).str.strip()")
        data_token.Words = convert.remove_punctuation(data_token['Words'])
        data_token = dataholder.remove_empty(data_token)
        data.Clean = convert.remove_punctuation(data.Clean) #Memanggil remove_punctuation pada convert, untuk menghilangkan tanda baca dan sebagainya pada teks
        selected_punct = st.selectbox( #Box pemilihan untuk memilih mode tampilan dataframe remove punct
            label='Select Dataframe Type',
            options=select_type_dataframe,
            key='selectpunct'
        )
        if(selected_punct == select_type_dataframe[0]):
            st.dataframe(data=data_token, width=1000)
            st.write(f'Panjang data token menjadi : {data_token.shape[0]}')
        else:
            st.dataframe(data=data.head(),width=1000*len(data.columns)) #Menampilkan hasil dari penghapusan tanda baca
################################################################################################################################################################################


################################################################################################################################################################################
        st.subheader(f'Removing Unwanted Characters')
        st.write(f'Menghilangkan kurung buka, kurung tutup, \'\\n \', \'\\t\' dan sebagainya menggunakan regex')
        st.code("df.apply(lambda x: re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])').sub('',re.compile(r'<[^>]+>').sub('' ,re.sub('\s+', ' ',x )))")
        data.Clean = convert.remove_unwanted(data.Clean) #Memanggil remove_unwanted pada convert, untuk menghapus kata-kata yang tidak diinginkan pada teks
        data_token.Words = convert.remove_unwanted_ver2(data_token.Words)
        data_token = dataholder.remove_empty(data_token)
        selected_unwanted = st.selectbox( #Box pemilihan untuk memilih mode tampilan dataframe unwanted char
            label='Select Dataframe Type',
            options=select_type_dataframe,
            key='selectunwanted'
        )
        if( selected_unwanted == select_type_dataframe[0]):
            st.dataframe(data=data_token, width=1000)
            st.write(f'Panjang data token menjadi : {data_token.shape[0]}')
        else:
            st.dataframe(data=data.head(),width=1000*len(data.columns)) #Menampilkan data setelah penghapusan kata yang tidak diinginkan
################################################################################################################################################################################


################################################################################################################################################################################
        st.subheader(f'Removing stop-words')
        select_stop = ['From NLTK','From Sastrawi', 'Both']
        selected_stop = st.selectbox( #Box pemilihan untuk memilih metode stop-words
            label='Select Stop Words Type',
            options=select_stop,
        )
        # st.write(f'{select_list.index(selected_stop)}')
        stop_words = stopstem.define_stop_words(select_stop.index(selected_stop)) #Memanggil define_stop_words untuk memanggil list stop-words akan akan digunakan
        data.Clean = convert.remove_stop_word(data.Clean,stop_word=stop_words) #Memanggil remove_stop_words untuk menghapus stop-words yang ada pada teks
        data_token.Words = convert.remove_stop_word(data_token.Words,stop_word=stop_words)
        data_token = dataholder.remove_empty(data_token)
        selected_unwanted = st.selectbox( #Box pemilihan untuk memilih mode tampilan dataframe stop-words
            label='Select Dataframe Type',
            options=select_type_dataframe,
            key='selectwstopword'
        )
        if( selected_unwanted == select_type_dataframe[0]):
            st.dataframe(data=data_token, width=1000)
            st.write(f'Panjang data token menjadi : {data_token.shape[0]}')
        else:
            st.dataframe(data=data.head(),width=1000*len(data.columns)) #Menampilkan hasil setelah penghapusan stop-words

        try: #Coba minta input dari user
            get_text_drop_from_user = st.text_input(label='Atau, tambahkan stop-words yang anda inginkan (dipisahkan dengan koma)',placeholder='Ketik disini!') #Box text untuk user memasukkan stop-words tambahan
            if(len(get_text_drop_from_user)!=0):
                st.write(f'Data setelah remove stop-words user')
                data.Clean = convert.remove_stop_word(data.Clean, stop_word=get_text_drop_from_user.split(','))
                st.dataframe(data=data.head(),width=1000*len(data.columns)) #Memanggil remove_stop_words untuk menghapus stop-words dengan stop-words tambahan dari user
        except:
            pass
################################################################################################################################################################################


################################################################################################################################################################################

        st.subheader(f'Change text')
        all_change = st.text_area(label=f'Ubah kata-kata menjadi sebuah kata baru (contoh: bgs = bagus, krn = keren) pisahkan dengan koma!',placeholder='Ketik disini!'
                                  ,value=change_text.changed)
        all_change = all_change.split(',')
        data.Clean = dataholder.replace_all(data.Clean,all_change,1)
        data_token.Words = dataholder.replace_all(data_token.Words,all_change,0)
        data_token = dataholder.remove_empty(data_token)
        selected_unwanted = st.selectbox( #Box pemilihan untuk memilih mode tampilan dataframe change text
            label='Select Dataframe Type',
            options=select_type_dataframe,
            key='selectchange'
        )
        if( selected_unwanted == select_type_dataframe[0]):
            st.dataframe(data=data_token, width=1000)
            st.write(f'Panjang data token menjadi : {data_token.shape[0]}')
        else:
            st.dataframe(data=data,width=1000*len(data.columns)) #Menampilkan hasil setelah change text
        # st.write(data=data_token,width=)
################################################################################################################################################################################


################################################################################################################################################################################
        st.subheader(f'Normalize Text')
        select_norm = ['Using Stemmer (Sastrawi)','Using Lemmatize (very very slow!, i\'m using kbbi web-scraping to normalize)']
        selected_norm = st.selectbox( #Box pemilihan untuk memilih metode stop-words
            label='Select Normalize Type',
            options=select_norm
        )
        data.Clean = stopstem.define_normalizer(data.Clean,select_norm.index(selected_norm)) #Memanggil define_normalizer yang berguna untuk melakukan normalisasi pada data yang ingin dibersihkan
        data_token.Words = stopstem.define_normalizer(data_token.Words,select_norm.index(selected_norm))
        data_token = dataholder.remove_empty(data_token)
        selected_unwanted = st.selectbox( #Box pemilihan untuk memilih mode tampilan dataframe normalize
            label='Select Dataframe Type',
            options=select_type_dataframe,
            key='selectnormalize'
        )
        if( selected_unwanted == select_type_dataframe[0]):
            st.dataframe(data=data_token, width=1000)
        else:
            st.dataframe(data=data,width=1000*len(data.columns)) #Menampilkan data yang telah di normalisasi
        if(select_norm.index(selected_norm)==1):
            st.write('#Notes : Ada limit dalam pencarian menggunakakn KBBI Web, jika tidak terjadi perubahan, maka itu menandakan bahwa sudah menyentuh LIMIT🙏') #Notes ketika metode normalisasi yang dipilih merupakan Lematisasi
################################################################################################################################################################################


################################################################################################################################################################################
        st.subheader(f'One-Hot Encoding (Clean Data)')
        st.write(f'One-Hot Encoding secara menual dengan melakukan enumerasi terhadap setiap unique values yang terdapat pada kalimat')
        onehot = dataholder.make_one_hot(data.Clean) #Memanggil make_one_hot pada dataholder untuk membuat sebuah One-Hot-Encoding
        st.dataframe(data=onehot,width=100*len(onehot.columns)) #Menampilkan hasil One-Hot-Encoding
################################################################################################################################################################################


################################################################################################################################################################################
        st.subheader(f'Bags of Words (Clean Data)')
        st.write(f'Bags of words secara manual dengan algoritma serupa dengan One-Hot Encoding')
        bags_of_words = dataholder.make_bag_of_words(data.Clean) #Memanggil make_bag_of_words pada dataholder untuk membuat sebuah Bag of Words tabel
        st.dataframe(data=bags_of_words,width=100*len(bags_of_words.columns)) #Menampilkan data Bag of Words
################################################################################################################################################################################


################################################################################################################################################################################
        st.subheader(f'TF-IDF Bags Of Words Values')
        # st.write(f'')
        bags_of_words = dataholder.get_tf_idf_value(bags_of_words)#Memanggil get_tf_idf_value pada dataholder yang berfungsi untuk menghasilkan data TF-IDF yang ada pada data
        st.dataframe(data=bags_of_words)#Menampilkan data Bags of Words yang telah diisikan dengan tabel TF-IDF
################################################################################################################################################################################
    except Exception as e:
        st.error(f'Error Pada Data!')
        st.write(e)

if __name__== '__main__':
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Program')
    with col2:
        st.header('Sentimen')
        st.image(dataholder.get_images('hero'),width=150,caption='Made By Pande Dani, Informatika 2021') #Foto Profile & Nama Developer
    with col3:
        st.header('Analisis')

    try:
        get_num = int(st.text_input(label='Masukkan Nomor Absen',placeholder='Ketik Disini!',value='5'))
        if(get_num<1 or get_num>20):
            raise NameError
        get_progress()
        
    except Exception as e:
        st.error('Nomor absen harus diantara 1 - 20!')
    
#Dibuat oleh Pande Dani