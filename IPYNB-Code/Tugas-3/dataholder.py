import pandas as pd
import numpy as np
from pathlib import Path
import math
from PIL import Image

PATH = Path(__file__).parent.parent.parent
DDIR = PATH / 'datasets'
IMGDIR = PATH / 'images'

df = pd.read_excel(f'{DDIR}/Dataset B.xlsx')


def get_sample(df, num:int):
    df = df.iloc[num*10-10:num*10,:]
    return df

def drop_column(df, dropped:list):
    df = df.drop(columns=dropped)
    return df

def make_bag_of_words(df):
    list_unique = np.array([],dtype=str)
    for x in df.values:
        list_unique = np.append(list_unique, list(set(x.split())))
    list_unique = np.unique(list_unique)
    num_unique = len(list_unique)
    return bag_of_words_data_maker(df, list_unique, num_unique)
    
def bag_of_words_data_maker(df, list_unq, num_unq):
    init_data = np.zeros((num_unq, len(df)),dtype=int)
    bag_of_words = pd.DataFrame(init_data)
    bag_of_words['Words'] = list_unq
    for key,x in enumerate(df.index.values):
        bag_of_words.rename(columns={key:x},inplace=True)
    bag_of_words.set_index('Words',inplace=True)
    for key,value in df.iteritems():
        for key2,value2 in enumerate(list_unq):
            bag_of_words[key].iloc[key2] = value.split().count(value2)
    return bag_of_words

def make_one_hot(df):
    list_unique = np.array([],dtype=str)
    for x in df.values:
        list_unique = np.append(list_unique, list(set(x.split())))
    list_unique = np.unique(list_unique)
    num_unique = len(list_unique)
    return one_hot_data_maker(df, list_unique, num_unique)

def one_hot_data_maker(df, list_unq, num_unq):
    init_data = np.zeros((num_unq, len(df)),dtype=int)
    onehot = pd.DataFrame(init_data)
    onehot['Words'] = list_unq
    for key,x in enumerate(df.index.values):
        onehot.rename(columns={key:x},inplace=True)
    onehot.set_index('Words',inplace=True)
    for key,value in df.iteritems():
        for key2,value2 in enumerate(list_unq):
            onehot[key].iloc[key2] = 1 if value.split().count(value2) > 0 else 0
    return onehot

def get_tf_idf_value(df):
    #IDF = number of columns / rows value
    list_idf = np.array([],dtype=float)
    for key,value in df.iterrows():
        try:
            value = round(math.log(len(df.columns)/value.sum()),3)
        except:
            value = 0
        list_idf = np.append(list_idf, value)
    
    #TF = value / columns sum

    #TF-IDF = IDF * TF
    for x in df.columns:
        list_tf = np.array([],dtype=float)
        columns_sum = df[x].sum()
        for y in range(len(df[x])):
            try:
                value = round((df[x].iloc[y] / columns_sum) * list_idf[y],3)
            except:
                value = 0
            list_tf = np.append(list_tf, value)
        df[f'{x} TF-IDF-Score'] = list_tf

    return df
        
    
def get_images(name):
    image = Image.open(f'{IMGDIR}/{name}.jpg')
    return image



