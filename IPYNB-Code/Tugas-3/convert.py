import string
import re

TAG_RE = re.compile(r'<[^>]+>')
RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')

def make_lower(df):
    data = df.str.lower() #Lowercasing
    return data

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

def remove_stop_word(df, stop_word):
    data = df.apply(lambda x: ' '.join([kata for kata in x.split() if kata not in stop_word])) #Menghapus stop-words pada teks
    return data