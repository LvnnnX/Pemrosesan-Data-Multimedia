import streamlit as st
import dataholder
import convert
import stopstem
from PIL import Image
# import pandas as pd

def get_progress():
    try:
        data = dataholder.get_sample(dataholder.df,get_num)
        st.write('##')
        st.subheader('Sample Data')
        st.dataframe(data=data.head(),width=1000*len(data.columns))

        st.write("##")
        st.subheader('Drop No Column')
        st.write(f'Karena kolom \'No\' tidak memiliki pengaruh terhadap data (residual) maka kita drop kolom \'No\'')
        data = dataholder.drop_column(data,['No'])
        st.dataframe(data=data.head(),width=1000*len(data.columns))

        st.write('##')
        st.header(f'Preprocessing')
        st.subheader(f'Lowercasing')
        st.write(f'Mengubah text menjadi lowercase menggunakan .lower()')
        st.code(".str.lower()")
        data['Clean'] = convert.make_lower(data.Reviews)
        data = convert.change_column(data)
        st.dataframe(data=data.head(),width=1000*len(data.columns))

        # st.write('##')
        st.subheader(f'Removing Digits')
        st.write(f'Menghilangkan digit pada text menggunakan .replace()')
        st.code(".str.replace('\d+','')")
        data.Clean = convert.remove_digit(data.Clean)
        st.dataframe(data=data.head(),width=1000*len(data.columns))

        st.subheader(f'Removing Punctuation')
        st.write(f'Menghilangkan tanda baca, tautan (links), dan whitespaces menggunakan .translate().strip()')
        st.code(".str.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).str.strip()")
        data.Clean = convert.remove_punctuation(data.Clean)
        st.dataframe(data=data.head(),width=1000*len(data.columns))

        st.subheader(f'Removing Unwanted Characters')
        st.write(f'Menghilangkan kurung buka, kurung tutup, \'\\n \', \'\\t\' dan sebagainya menggunakan regex')
        st.code("df.apply(lambda x: re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])').sub('',re.compile(r'<[^>]+>').sub('' ,re.sub('\s+', ' ',x )))")
        data.Clean = convert.remove_unwanted(data.Clean)
        st.dataframe(data=data.head(),width=1000*len(data.columns))


        st.subheader(f'Removing stop-words')
        select_stop = ['From NLTK','From Sastrawi', 'Both']
        selected_stop = st.selectbox(
            label='Select Stop Words Type',
            key=select_stop,
        )
        # st.write(f'{select_list.index(selected_stop)}')
        stop_words = stopstem.define_stop_words(select_stop.index(selected_stop))
        data.Clean = convert.remove_stop_word(data.Clean,stop_word=stop_words)
        st.dataframe(data=data.head(),width=1000*len(data.columns))

        try:
            get_text_drop_from_user = st.text_input(label='Atau, tambahkan stop-words yang anda inginkan (dipisahkan dengan koma)',placeholder='Ketik disini!')
            if(len(get_text_drop_from_user)!=0):
                st.write(f'Data setelah remove stop-words user')
                data.Clean = convert.remove_stop_word(data.Clean, stop_word=get_text_drop_from_user.split(','))
                st.dataframe(data=data.head(),width=1000*len(data.columns))
                pass
        except:
            pass

        st.subheader(f'Normalize Text')
        select_norm = ['Using Stemmer (Sastrawi)','Using Lemmatize (very very slow!, i\'m using kbbi web-scraping to normalize)']
        selected_norm = st.selectbox(
            label='Select Normalize Type',
            key=select_norm
        )
        data.Clean = stopstem.define_normalizer(data.Clean,select_norm.index(selected_norm))
        st.dataframe(data=data,width=1000*len(data.columns))
        if(select_norm.index(selected_norm)==1):
            st.write('#Notes : Ada limit dalam pencarian menggunakakn KBBI Web, jika tidak terjadi perubahan, maka itu menandakan bahwa sudah menyentuh LIMIT🙏')

        st.subheader(f'One-Hot Encoding (Clean Data)')
        st.write(f'One-Hot Encoding secara menual dengan melakukan enumerasi terhadap setiap unique values yang terdapat pada kalimat')
        onehot = dataholder.make_one_hot(data.Clean)
        st.dataframe(data=onehot,width=100*len(onehot.columns))

        st.subheader(f'Bags of Words (Clean Data)')
        st.write(f'Bags of words secara manual dengan algoritma serupa dengan One-Hot Encoding')
        bags_of_words = dataholder.make_bag_of_words(data.Clean)
        st.dataframe(data=bags_of_words,width=100*len(bags_of_words.columns))

        st.subheader(f'TF-IDF Bags Of Words Values')
        st.write(f'..')
        onehot = dataholder.get_tf_idf_value(onehot)
        st.dataframe(onehot)

    except Exception as e:
        st.error(f'Error Pada Data!')
        st.write(e)

if __name__== '__main__':
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Program')
    with col2:
        st.header('Sentimen')
        st.image(dataholder.get_images('hero'),width=150,caption='Made By Pande Dani, Informatika 2021')
    with col3:
        st.header('Analisis')

    try:
        get_num = int(st.text_input(label='',placeholder='Masukkan Nomor Absen'))
        if(get_num<1 or get_num>20):
            raise NameError
        get_progress()
        
    except Exception as e:
        st.error('Nomor absen harus diantara 1 - 20!')
    