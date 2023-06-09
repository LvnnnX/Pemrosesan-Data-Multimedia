from nltk.corpus import stopwords
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from kbbi import KBBI


nltk.download('stopwords')
stem_factory = StemmerFactory()
stemmer = stem_factory.create_stemmer()
stop_factory = StopWordRemoverFactory()

def iterate_lemma(kata):
    try:
        kata = str(KBBI(kata)).split()[0].replace('.','') #Menggunakan KBBI untuk mencari kata dasar
    except:
        kata = kata #kalau error atau tidak ketemu, maka kata tidak berubah
    return kata

def lemmatize(df):
    data = df.apply(lambda x: ' '.join([iterate_lemma(kata) for kata in x.split()])) #Mengganti kata menjadi kata dasar menggunakan KBBI API
    return data

def stemming(df):
    data = df.apply(lambda x: stemmer.stem(x)) #Mengganti menjadi kata dasar menggunakan Sastrawi.Stemmer
    # for x in range(len(df)):
        # datax = df.iloc[x].split()
        # for y in range(len(datax)):
        #     datax[y] = stemmer.stem(datax[y])
        # df.iloc[x] = ' '.join(datax)
        # df.iloc[x] = stemmer.stem(df.iloc[x])
    return data

def define_stop_words(num:int): #Pilihan user pada box pilihan stop-words
    if(num==0):
        stop_word = stopwords.words('indonesian') + stopwords.words('english')
    elif(num==1):
        stop_word = stop_factory.get_stop_words()
    elif(num==2):
        stop_word = list(set(stopwords.words('indonesian') + stopwords.words('english') + stop_factory.get_stop_words()))
    else:
        raise ValueError
    return stop_word

def define_normalizer(df, num:int): #pilihan user pada box pilihan normalisasi teks
    if(num==0):
        return stemming(df=df)
    elif(num==1):
        return lemmatize(df=df)
    else:
        raise NameError
