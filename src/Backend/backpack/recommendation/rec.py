## REcommend BOoks related to certain book.
## Called from ITem description page with particular book 
## output similar books 
## Set 15 items to return default. Can Change.

import numpy as np
import pandas as pd
import pickle
from gensim.models.word2vec import Word2Vec
df = pd.read_csv('/home/sweteam4/test/test/data/booklec.csv')

df['major'] = df['major'].apply(lambda x : 18 if x == 38 else x)

df_major = df[df['difficulty']>=2]
df_minor = df[df['difficulty']==1]

b2b = Word2Vec.load('/home/sweteam4/test/test/model/b2b.model')
id2book = open("/home/sweteam4/test/test/data/id_2_book_name.pkl", "rb")
lec2book = open("/home/sweteam4/test/test/data/lecture_2_book_name.pkl", "rb")


class rec_item:
    def __init__(self, top_n = 30, name='selectedBook_Recommender'):
        #self.predict(item)
        self.name = name
        self.top_n = top_n

    def predict(self, item, other = False): #other 변수는 만약 다른 학과과목을 추천받고싶다면 true로넣어주면 다른과 위주.
        top_n = self.top_n;
        item_tuple = b2b.wv.most_similar(positive=item, topn = top_n)
        item_list = []
        for i in range(top_n):
            item_list.append(list(item_tuple[i]))
        maj = df[df['bk'] == item]['major'].values[0]
        dif = df[df['bk'] == item]['difficulty'].values[0]

        for i in range(top_n):
            if df[df['bk'] == item_list[i][0]]['major'].values[0] == maj:
                if other:
                    item_list[i][1] = item_list[i][1] * 0.5
            else: # if book, rec book has dif major
                if not(other): # if !other(want related to major)
                    item_list[i][1] = item_list[i][1] * 0.6

            if df[df['bk'] == item_list[i][0]]['difficulty'].values[0] > dif:
                item_list[i][1] = item_list[i][1] * 1
            elif df[df['bk'] == item_list[i][0]]['difficulty'].values[0] == dif:
                item_list[i][1] = item_list[i][1] * 0.9
            else: # if book, rec book has dif major
                if not(other):
                    item_list[i][1] = item_list[i][1] * 0.5

        final_list = np.array(sorted(item_list, key=lambda x : x[1], reverse=True))[:,0][:10]
        return final_list


cla = rec_item('컴퓨터 네트워킹 : 하향식 접근(7판)')
print(cla.predict('컴퓨터 네트워킹 : 하향식 접근(7판)',True))




