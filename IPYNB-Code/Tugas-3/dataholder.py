import pandas as pd
import numpy as np
from pathlib import Path
import math
import re
from PIL import Image

PATH = Path(__file__).parent.parent.parent #Membuat Base Directory, Karena berada pada PDM/IPYNB-Code/Tugas-3, harus keluar directory sebanyak 3x
DDIR = PATH / 'datasets' #Directory untuk datasets
IMGDIR = PATH / 'Images' #Directory untuk gambar

df = pd.read_excel(f'{DDIR}/Dataset B.xlsx') #Mengambil Dataset B

def get_sample(df, num:int):
    df = df.iloc[num*10-10:num*10,:] #Memilih 10 ulasan dengan rumus = Rentangan data(x) = no absen*10-10 < x < no absen * 10
    return df #mengembalikan return berupa dataframe

def drop_column(df, dropped:list):
    df = df.drop(columns=dropped) #Membuang kolom
    return df

def remove_empty(df):
    df = df.replace('' , np.nan)
    df.drop_duplicates(keep='first',inplace=True)
    df.dropna(inplace=True)
    df.reset_index(drop=True,inplace=True)
    return df

def make_bag_of_words(df):
    list_unique = np.array([],dtype=str) #sebuah list yang terbuat dari numpy agar kompilasi lebih cepat
    for x in df.values:
        list_unique = np.append(list_unique, list(set(x.split()))) #Mengambil unique word (kata unik) yang ada pada teks dan memasukkannya kedalam list
    list_unique = np.unique(list_unique) #Mengambil unique word pada list sendiri, karena kemungkinan terjadi duplikasi pada perintah sebelumnya
    num_unique = len(list_unique) #Panjang dari data unique
    return bag_of_words_data_maker(df, list_unique, num_unique) #Memanggil fungsi bag_of_words_data_maker
    
def bag_of_words_data_maker(df, list_unq, num_unq):
    init_data = np.zeros((num_unq, len(df)),dtype=int) #membuat sebuah matrix kosong dengan besaran baris = banyaknya kata unik dan kolom = banyaknya data (10)
    bag_of_words = pd.DataFrame(init_data) #Mengubah matrix menjadi dataframe agar memudahkan visualisasi
    bag_of_words['Words'] = list_unq #Menambahkan kolom 'Words' pada dataframe
    for key,x in enumerate(df.index.values):
        bag_of_words.rename(columns={key:x},inplace=True) #Mengganti nama header kolom menjadi nama ID / Dokumen pada data sebelumnya
    bag_of_words.set_index('Words',inplace=True) #Menjadikan kolom 'Words' sebagai index
    for key,value in df.iteritems():
        for key2,value2 in enumerate(list_unq):
            bag_of_words[key].iloc[key2] = value.split().count(value2) #Mengubah value dari elemen dataframe dengan jumlah kata yang terdeteksi
    return bag_of_words #Mengembalikan dataframe

def make_one_hot(df):
    list_unique = np.array([],dtype=str)#sebuah list yang terbuat dari numpy agar kompilasi lebih cepat
    for x in df.values:
        list_unique = np.append(list_unique, list(set(x.split()))) #Mengambil unique word (kata unik) yang ada pada teks dan memasukkannya kedalam list
    list_unique = np.unique(list_unique) #Mengambil unique word pada list sendiri, karena kemungkinan terjadi duplikasi pada perintah sebelumnya
    num_unique = len(list_unique) #Panjang dari data unique
    return one_hot_data_maker(df, list_unique, num_unique) #Memanggil fungsi one_hot_data_maker

def one_hot_data_maker(df, list_unq, num_unq):
    init_data = np.zeros((num_unq, len(df)),dtype=int)#membuat sebuah matrix kosong dengan besaran baris = banyaknya kata unik dan kolom = banyaknya data (10)
    onehot = pd.DataFrame(init_data)#Mengubah matrix menjadi dataframe agar memudahkan visualisasi
    onehot['Words'] = list_unq #Menambahkan kolom 'Words' pada dataframe
    for key,x in enumerate(df.index.values):
        onehot.rename(columns={key:x},inplace=True) #Mengganti nama header kolom menjadi nama ID / Dokumen pada data sebelumnya
    onehot.set_index('Words',inplace=True) #Menjadikan kolom 'Words' sebagai index
    for key,value in df.iteritems():
        for key2,value2 in enumerate(list_unq):
            onehot[key].iloc[key2] = 1 if value.split().count(value2) > 0 else 0 #Mengubah value dari elemen dataframe dengan 1 jika ada kata terdeteksi, 0 jika tidak
    return onehot #Mengembalikan dataframe

def get_tf_idf_value(df):
    #IDF = number of columns / rows value
    list_idf = np.array([],dtype=float) #List untuk menampung IDF matrix
    for key,value in df.iterrows():
        try:
            value = round(math.log(len(df.columns)/value.sum()),3) #Mencari IDF dengan rumus IDF(value-x) = banyaknya kolom / value-x
        except:
            value = 0 #Jika value-x = 0, rumus tidak bisa dijalankan karena akan membagi dengan 0, jadi tetapkan value menjadi 0
        list_idf = np.append(list_idf, value) #menambahkan hasil kedalam list
    
    #TF = value / columns sum

    #TF-IDF = IDF * TF
    for x in df.columns:
        list_tf = np.array([],dtype=float)
        columns_sum = df[x].sum() #Banyaknya kolom
        for y in range(len(df[x])):
            try:
                value = round((df[x].iloc[y] / columns_sum) * list_idf[y],3) #Menggunakan rumus TF * IDF
            except:
                value = 0
            list_tf = np.append(list_tf, value) #menambahkan kedalam list
        df[f'{x} TF-IDF-Score'] = list_tf #menambahkan tabel TF-IDF pada dataframe

    return df #mengembalikan dataframe
        
    
def get_images(name):
    image = Image.open(f'{IMGDIR}/{name}.jpg') #Mengambil gambar pada directory images
    return image #mengembalikan value berupa gambar


def replace_all(df,list_replace:list,mode:int):
    for string in list_replace:
        isi_string = string.split('=') #pisahkan input dengan pemisahan yaitu =
        kiri = isi_string[0].strip() #pemisahan bagian kiri
        kanan = isi_string[1].strip() #pemisahan bagian kanan
        if(mode==0):
            df.replace(kiri,kanan,inplace=True) #replace kata ini
        elif(mode==1): 
            df = df.apply(lambda x: re.sub(kiri,kanan,x)) #replace kata di dataframe
        else: 
            raise NameError
    return df


#Dibuat oleh Pande Dani