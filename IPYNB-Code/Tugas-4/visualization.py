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


def color_histogram(type:str, num_allowed:list):
    if(type!='all'):
        fig, ax = plt.subplots(nrows=len(num_allowed)//5, ncols=5, figsize=(50,15), dpi=100)
        for num,image in enumerate(num_allowed):
            sns.set(style="darkgrid")
            test_data = io.imread(f'{DDIR}/{type}/{type}-{image:04d}.jpg')
            test_data = np.reshape(test_data, (48*48))
            # print(np.shape(test_data))
            ax[num//5][num%5].hist(test_data, bins=255, color='red', alpha=0.7, rwidth=0.85)
            ax[num//5][num%5].set_title(f'{type.capitalize()}-{image:04d} colour histogram', weight='bold')
            ax[num//5][num%5].set_xlim(-5,260)
            # ax[num//5][num%5].set_ylim(0,200)
            ax[num//5][num%5].set_xlabel('Colour distribution')
            ax[num//5][num%5].set_ylabel('Count',rotation=0,labelpad=20)
            # print(test_data.min(), test_data.max())
            # print(test_data)
    elif(type=='all'):
        fig, ax = plt.subplots(nrows=len(num_allowed), ncols=3, figsize=(10,25), dpi=100)
        for type_num,value in enumerate(['happy','sad','neutral']):
            for num,image in enumerate(num_allowed):
                sns.set_style('whitegrid')
                test_data = io.imread(f'{DDIR}/{value}/{value}-{image:04d}.jpg')
                test_data = np.reshape(test_data, (48*48))
                # print(np.shape(test_data))
                ax[num][type_num].hist(test_data, bins=255, color='red', alpha=0.7, rwidth=0.85)
                ax[num][type_num].set_title(f'{value.capitalize()}-{image:04d} colour histogram', weight='bold')
                ax[num][type_num].set_xlim(-5,260)
                # ax[num][type_num].set_ylim(0,200)
                ax[num][type_num].set_xlabel('Colour distribution')
                ax[num][type_num].set_ylabel('Count',rotation=0,labelpad=20)
                # print(test_data.min(), test_data.max())
                # print(test_data)
        plt.tight_layout()
    return fig

def texture_histogram(type:str,df:pd.DataFrame):
    df = df.T
    list_type = [x for x in df.columns if x.__contains__(type)]
    sns.set()
    df['Label'] = df.index
    fig,ax = plt.subplots(nrows=2,ncols=2,figsize=(20,10))
    for num,value in enumerate(list_type):
        ax[num//2][num%2].bar(df['Label'], df[value])
        ax[num//2][num%2].set_xticklabels(df['Label'], rotation=45)
        ax[num//2][num%2].set_title(f'{value.capitalize()} histogram', weight='bold')
    fig.suptitle(f'{type.capitalize()} histogram', weight='bold', fontsize=20)
    plt.tight_layout()
    return fig