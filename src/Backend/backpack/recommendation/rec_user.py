## Recommend BOoks related to list of books
## Called from Main or other pages with list of books that particular user bought.(history)
## output similar books.
## Set 15 items to return default. Can change.
## should add feature axis that make priorities between 15 items.

import numpy as np
import pandas as pd
import pickle
from gensim.models.word2vec import Word2Vec
from collections import Counter
df = pd.read_csv('/home/sweteam4/test/test/data/booklec.csv')

df['major'] = df['major'].apply(lambda x : 18 if x == 38 else x)

df_major = df[df['difficulty']>=2]
df_minor = df[df['difficulty']==1]

b2b = Word2Vec.load('/home/sweteam4/test/test/model/b2b.model')
id2book = open("/home/sweteam4/test/test/data/id_2_book_name.pkl", "rb")
lec2book = open("/home/sweteam4/test/test/data/lecture_2_book_name.pkl", "rb")


class rec_user_item:
    def __init__(self, top_n = 30, name='FromUserHistory_Recommender'):
        self.name = name
        self.top_n = top_n


    def predict(self, items, user_grade=None, user_major=None, neg_items=None):
        # 추후에 neg_item 이용해서 싫어하는 종류를 고를수있고 이를 추천에서 제외가능.
        # user_major는 user major에 따라서, 최근 history에 따라서 두개 추천가능.
        item_tuple = b2b.wv.most_similar(positive=items, negative=neg_items, topn = top_n)
        item_list = []

        for i in range(top_n):
            item_list.append(list(item_tuple[i]))
        ls1 = [df[df['bk'] == item_list[i][0]]['major'].values[0] for i in range(top_n)]
        maj = Counter(ls1).most_common(1)[0][0]
        ls2 = [df[df['bk'] == item_list[i][0]]['difficulty'].values[0] for i in range(top_n)]
        dif = np.mean(ls2)
        maj = df[df['bk'] == user_major]['major'].values[0]
        dif2 = df[df['bk'] == user_grade]['difficulty'].values[0]
        dif = (dif + dif2)/2
        for i in range(top_n):
            if df[df['bk'] == item_list[i][0]]['difficulty'].values[0] == maj:
                ;
            else:
                item_list[i][1] = item_list[i][1] * 0.6

            if df[df['bk'] == item_list[i][0]]['difficulty'].values[0] - dif > 1:
                item_list[i][1] = item_list[i][1] * 0.9
            elif df[df['bk'] == item_list[i][0]]['difficulty'].values[0] - dif >= -0.2:
                item_list[i][1] = item_list[i][1] * 1.0
            elif df[df['bk'] == item_list[i][0]]['difficulty'].values[0] - dif >= -1:
                item_list[i][1] = item_list[i][1] * 0.6
            else: # if rec book is easier
                item_list[i][1] = item_list[i][1] * 0.4

        final_list = np.array(sorted(item_list, key=lambda x: x[1], reverse=True))[:,0][:10]


 
 
 
        return final_list









