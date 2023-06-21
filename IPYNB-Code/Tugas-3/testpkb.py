import pandas as pd
from dataholder import make_one_hot, make_bag_of_words

teks = ['data science is one of the most important fields of science',
          'this is one of the best data science courses',
          'data scientists analyze data']

df = pd.DataFrame(teks)

make_one_hot(df)