import string
import re
import numpy as np
import pandas as pd
import spacy
import dataholder

nlp = spacy.blank('id')

TAG_RE = re.compile(r'<[^>]+>')
RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')

def tokenize(df):
    list_token = np.array([],dtype=str)
    for x in df:
        list_token = np.append(list_token, nlp(x))
    data_token = pd.DataFrame(list_token,columns=['Words'])
    return data_token

def make_lower(df):
    df = df.apply(lambda x: str(x).lower())
    return df

def remove_digit(df):
    data = df.str.replace('\d+', '') #Mengganti digit dengan None atau kosong
    return data

def remove_punctuation(df):
    data = df.str.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).str.strip() #Menghapus tanda baca pada teks
    return data

def change_column(df):
    cols = ['Reviews','Clean','Label']
    data = df[cols] #Mengganti urutan kolom pada dataframe
    return data

def remove_unwanted(df):
    data = df.apply(lambda x: RE_EMOJI.sub('',TAG_RE.sub('' ,re.sub('\s+', ' ',x )))) #Mengganti Emoji, Hastag, tanda <>?: dan seabgainya pada teks
    return data

def remove_unwanted_ver2(df):
    data = df.apply(lambda x: re.sub('\s+', '', str(x)))
    data = dataholder.remove_empty(data)
    data = df.apply(lambda x: TAG_RE.sub('', str(x)))
    data = dataholder.remove_empty(data)
    data = df.apply(lambda x: RE_EMOJI.sub('', str(x)))
    return data

def remove_stop_word(df, stop_word):
    data = df.apply(lambda x: ' '.join([kata for kata in x.split() if kata not in stop_word])) #Menghapus stop-words pada teks
    return data
