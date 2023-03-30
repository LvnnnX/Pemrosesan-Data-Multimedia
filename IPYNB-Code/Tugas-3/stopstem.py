from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import spacy
from kbbi import KBBI

nlp=spacy.blank('id')
stem_factory = StemmerFactory()
stemmer = stem_factory.create_stemmer()
stop_factory = StopWordRemoverFactory()

def iterate_lemma(kata):
    try:
        kata = str(KBBI(kata)).split()[0].replace('.','')
    except:
        kata = kata
    return kata

def lemmatize(df):
    data = df.apply(lambda x: ' '.join([iterate_lemma(kata) for kata in x.split()]))
    return data

def stemming(df):
    # data = df.apply(lambda x: stemmer.stem(x))
    for x in range(len(df)):
        datax = df.iloc[x].split()
        for y in range(len(datax)):
            datax[y] = stemmer.stem(datax[y])
        df.iloc[x] = ' '.join(datax)
    return df

def define_stop_words(num:int):
    if(num==0):
        stop_word = stopwords.words('indonesian')
    elif(num==1):
        stop_word = stop_factory.get_stop_words()
    elif(num==2):
        stop_word = list(set(stopwords.words('indonesian') + stop_factory.get_stop_words()))
    else:
        raise ValueError
    return stop_word

def define_normalizer(df, num:int):
    if(num==0):
        return stemming(df=df)
    elif(num==1):
        return lemmatize(df=df)
    else:
        raise NameError
