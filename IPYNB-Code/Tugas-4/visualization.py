import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from skimage import io
from pathlib import Path

PATH = Path(__file__).parent.parent.parent #Membuat Base Directory, Karena berada pada PDM/IPYNB-Code/Tugas-3, harus keluar directory sebanyak 3x
DDIR = PATH / 'datasets' #Directory untuk datasets
IMGDIR = PATH / 'Images' #Directory untuk gambar

HAPPY_DIR = DDIR / 'happy' #Directory untuk happy
SAD_DIR = DDIR / 'sad' #Directory untuk sad
NEUTRAL_DIR = DDIR / 'neutral' #Directory untuk neutral

def color_histogram(type:str, num_allowed:list): #Fungsi untuk membuat histogram warna
    if(type!='all'): #Jika type bukan all, maka akan membuat histogram warna untuk satu jenis
        fig, ax = plt.subplots(nrows=len(num_allowed)//5, ncols=5, figsize=(50,15), dpi=100) #Membuat subplot
        for num,image in enumerate(num_allowed): #Looping untuk membuat histogram warna
            sns.set(style="whitegrid") #Mengatur style
            test_data = io.imread(f'{DDIR}/{type}/{type}-{image:04d}.jpg') #Membaca gambar
            test_data = np.reshape(test_data, (48*48)) #Mengubah ukuran gambar menjadi 1D dengan panjang 48x48
            # print(np.shape(test_data))
            ax[num//5][num%5].hist(test_data, bins=255, color='red', alpha=0.7, rwidth=0.85) #Membuat histogram warna
            ax[num//5][num%5].set_title(f'{type.capitalize()}-{image:04d} colour histogram', weight='bold') #Mengatur judul
            ax[num//5][num%5].set_xlim(-5,260) #Mengatur batas x
            # ax[num//5][num%5].set_ylim(0,200)
            ax[num//5][num%5].set_xlabel('Colour distribution') #Mengatur label x
            ax[num//5][num%5].set_ylabel('Count',rotation=0,labelpad=20) #Mengatur label y
            # print(test_data.min(), test_data.max())
            # print(test_data)
    elif(type=='all'): #Jika type adalah all, maka akan membuat histogram warna untuk semua jenis
        fig, ax = plt.subplots(nrows=len(num_allowed), ncols=3, figsize=(10,25), dpi=100) #Membuat subplot
        for type_num,value in enumerate(['happy','sad','neutral']): #Looping untuk membuat histogram warna
            for num,image in enumerate(num_allowed): #Looping untuk membuat histogram warna
                sns.set_style('whitegrid') #Mengatur style
                test_data = io.imread(f'{DDIR}/{value}/{value}-{image:04d}.jpg') #Membaca gambar
                test_data = np.reshape(test_data, (48*48)) #Mengubah ukuran gambar menjadi 1D dengan panjang 48x48
                # print(np.shape(test_data))
                ax[num][type_num].hist(test_data, bins=255, color='red', alpha=0.7, rwidth=0.85) #Membuat histogram warna
                ax[num][type_num].set_title(f'{value.capitalize()}-{image:04d} colour histogram', weight='bold') #Mengatur judul
                ax[num][type_num].set_xlim(-5,260) #Mengatur batas x
                # ax[num][type_num].set_ylim(0,200) 
                ax[num][type_num].set_xlabel('Colour distribution') #Mengatur label x
                ax[num][type_num].set_ylabel('Count',rotation=0,labelpad=20) #Mengatur label y
                # print(test_data.min(), test_data.max())
                # print(test_data)
        plt.tight_layout() #Mengatur layout agar tidak terlalu rapat
    return fig #Mengembalikan figure

def texture_histogram(type:str,df:pd.DataFrame): #Fungsi untuk membuat histogram tekstur
    df = df.T #Mengubah dataframe menjadi transpose
    list_type = [x for x in df.columns if x.__contains__(type)] #Membuat list untuk menampung nama kolom yang berisi type
    sns.set() #Mengatur style
    df['Label'] = df.index #Membuat kolom label 
    fig,ax = plt.subplots(nrows=2,ncols=2,figsize=(20,10)) #Membuat subplot
    for num,value in enumerate(list_type):
        ax[num//2][num%2].bar(df['Label'], df[value]) #Membuat histogram tekstur
        ax[num//2][num%2].set_xticklabels(df['Label'], rotation=45) #Mengatur label x
        ax[num//2][num%2].set_title(f'{value.capitalize()} histogram', weight='bold') #Mengatur judul
    fig.suptitle(f'{type.capitalize()} histogram', weight='bold', fontsize=20) #Mengatur judul utama
    plt.tight_layout() #Mengatur layout agar tidak terlalu rapat
    return fig #Mengembalikan figure