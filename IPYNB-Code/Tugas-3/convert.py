import string
import re

TAG_RE = re.compile(r'<[^>]+>')
RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')

def make_lower(df):
    data = df.str.lower()
    return data

def remove_digit(df):
    data = df.str.replace('\d+', '')
    return data

def remove_punctuation(df):
    data = df.str.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).str.strip()
    return data

def change_column(df):
    cols = ['Reviews','Clean','Label']
    data = df[cols]
    return data

def remove_unwanted(df):
    data = df.apply(lambda x: RE_EMOJI.sub('',TAG_RE.sub('' ,re.sub('\s+', ' ',x ))))
    return data

def remove_stop_word(df, stop_word):
    data = df.apply(lambda x: ' '.join([kata for kata in x.split() if kata not in stop_word]))
    return data