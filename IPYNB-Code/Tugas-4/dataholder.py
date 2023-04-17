import pandas as pd
import numpy as np
from pathlib import Path
import math
import re
from PIL import Image
from skimage import io
from scipy.stats import skew,kurtosis,entropy

PATH = Path(__file__).parent.parent.parent #Membuat Base Directory, Karena berada pada PDM/IPYNB-Code/Tugas-3, harus keluar directory sebanyak 3x
DDIR = PATH / 'datasets' #Directory untuk datasets
IMGDIR = PATH / 'Images' #Directory untuk gambar

HAPPY_DIR = DDIR / 'happy' #Directory untuk happy
SAD_DIR = DDIR / 'sad' #Directory untuk sad
NEUTRAL_DIR = DDIR / 'neutral' #Directory untuk neutral

def get_images(name):
    image = Image.open(f'{IMGDIR}/{name}.jpg') #Mengambil gambar pada directory images
    return image #mengembalikan value berupa gambar

def get_sample_image(type:str, num:int):
    image = io.imread(f'{DDIR}/{type}/{type}-{num:04d}.jpg') #Mengambil gambar pada directory datasets
    return image
def get_allowed_images_num(kelas:str,all_class:list, absen:int) -> list:
    allowed_min = 300 * (all_class.index(kelas)) + (10 * (absen-1)) + 1
    allowed_max = allowed_min + 9
    return list(range(allowed_min,allowed_max+1))

def get_one_matrix(num:int, type:str):
    return io.imread(f'{DDIR}/{type}/{type}-{num:04d}.jpg')

def get_all_matrix(num:list, type:list):
    all_matrix = []
    for i in type:
        for j in num:
            all_matrix.append(io.imread(f'{DDIR}/{i}/{i}-{j:04d}.jpg'))
    return all_matrix
    

def get_first_order_statistics(type:str, num_allowed:list) -> pd.DataFrame:
    image_name = []
    all_image = []
    first_order_dataframe = pd.DataFrame(columns=['Label','Mean','Variance','Skewness','Kurtosis','Entropy'])
    for num,value in enumerate(num_allowed):
        data_first_order = []
        image_data = io.imread(f'{DDIR}/{type}/{type}-{value:04d}.jpg')
        image_data = np.reshape(image_data, (48*48))
        data_first_order.append(f'{type}-{value:04d}')

        data_first_order.append(np.mean(image_data))

        data_first_order.append(np.var(image_data, dtype=np.float64))

        data_first_order.append(skew(image_data))

        data_first_order.append(kurtosis(image_data))

        data_first_order.append(entropy(image_data))
        first_order_dataframe.loc[len(first_order_dataframe)] = data_first_order

    first_order_dataframe.index=first_order_dataframe['Label']
    first_order_dataframe.drop(columns=['Label'], inplace=True)
    first_order_dataframe = first_order_dataframe.T
    return first_order_dataframe