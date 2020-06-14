from django.shortcuts import render
from rest_framework import viewsets, views
from django.http import JsonResponse
import numpy as np
import pandas as pd
import pickle
from gensim.models.word2vec import Word2Vec
from rest.models import Book, History
from django.core import serializers
from collections import Counter
from django.core import serializers


# Create your views here.

class rec_item(views.APIView):
    df = pd.read_csv('recommendation/data/booklec.csv')

    df['major'] = df['major'].apply(lambda x : 18 if x == 38 else x)

    df_major = df[df['difficulty']>=2]
    df_minor = df[df['difficulty']==1]

    b2b = Word2Vec.load('recommendation/data/b2b.model')
    # id2book = open("recommendation/data/id_2_book_name.pkl", "rb")
    # lec2book = open("recommendation/data/lecture_2_book_name.pkl", "rb")

    top_n = 30
   

    def post(self, request):
        item = request.POST.get('item')  # string
        other = request.POST.get('other')  # Boolean
        
        if other == 'false':
            flag = False
        else:
            flag = True

        result_list = self.predict(item, other=flag)
        
        # queryset to JSON
        book_list = list()
        for bk in result_list:
            try:
                book = Book.objects.get(bk = bk)

                book_dict = dict()

                book_dict['lec'] = book.lec
                book_dict['prof'] = book.prof
                book_dict['bk'] = book.bk
                book_dict['publisher'] = book.publisher
                book_dict['author'] = book.author
                book_dict['serial'] = book.serial
                book_dict['credit'] = book.credit
                book_dict['rating'] = book.rating
                book_dict['major'] = book.major
                book_dict['difficulty'] = book.difficulty
                book_dict['book_img'] = book.book_img.url
                
                book_list.append(book_dict)
            except:
                print("fail")
                continue

        return JsonResponse(book_list, safe=False)


    def predict(self, item, other = False): #other 변수는 만약 다른 학과과목을 추천받고싶다면 true로넣어주면 다른과 위주.
        item_tuple = self.b2b.wv.most_similar(positive=item, topn = self.top_n)
        item_list = []
        for i in range(self.top_n):
            item_list.append(list(item_tuple[i]))
        maj = self.df[self.df['bk'] == item]['major'].values[0]
        dif = self.df[self.df['bk'] == item]['difficulty'].values[0]

        for i in range(self.top_n):
            if self.df[self.df['bk'] == item_list[i][0]]['major'].values[0] == maj:
                if other:
                    item_list[i][1] = item_list[i][1] * 0.5
            else: # if book, rec book has dif major
                if not(other): # if !other(want related to major)
                    item_list[i][1] = item_list[i][1] * 0.1

            if self.df[self.df['bk'] == item_list[i][0]]['difficulty'].values[0] > dif:
                item_list[i][1] = item_list[i][1] * 1
            elif self.df[self.df['bk'] == item_list[i][0]]['difficulty'].values[0] == dif:
                item_list[i][1] = item_list[i][1] * 0.9
            else: # if book, rec book has dif major
                if not(other):
                    item_list[i][1] = item_list[i][1] * 0.5

        final_list = np.array(sorted(item_list, key=lambda x : x[1], reverse=True))[:, 0].tolist()

        return final_list


class rec_user_item(views.APIView):

    df = pd.read_csv('recommendation/data/booklec.csv')

    df['major'] = df['major'].apply(lambda x : 18 if x == 38 else x)

    df_major = df[df['difficulty']>=2]
    df_minor = df[df['difficulty']==1]

    b2b = Word2Vec.load('recommendation/data/b2b.model')
    # id2book = open("recommendation/data/id_2_book_name.pkl", "rb")
    # lec2book = open("recommendation/data/lecture_2_book_name.pkl", "rb")

    top_n = 30

    def post(self, request):
        user_id = request.POST.get('user_id')  # string

        histories = History.objects.filter(user_id = user_id)

        item_list = list()
        if histories is not None:
            for history in histories:
                bk = history.book_id.bk
                item_list.append(bk)
        else:
            return JsonResponse({'result': 'Empty history'})


        result_list = self.predict(items=item_list)

        # queryset to JSON
        book_list = list()
        for bk in result_list:
            try:
                book = Book.objects.get(bk = bk)

                book_dict = dict()

                book_dict['lec'] = book.lec
                book_dict['prof'] = book.prof
                book_dict['bk'] = book.bk
                book_dict['publisher'] = book.publisher
                book_dict['author'] = book.author
                book_dict['serial'] = book.serial
                book_dict['credit'] = book.credit
                book_dict['rating'] = book.rating
                book_dict['major'] = book.major
                book_dict['difficulty'] = book.difficulty
                book_dict['book_img'] = book.book_img.url
                
                book_list.append(book_dict)
            except:
                print("fail")
                continue

        return JsonResponse(book_list, safe=False)


    def predict(self, items, user_grade=None, user_major=None, neg_items=None):
        # 추후에 neg_item 이용해서 싫어하는 종류를 고를수있고 이를 추천에서 제외가능.
        # user_major는 user major에 따라서, 최근 history에 따라서 두개 추천가능.
        item_tuple = self.b2b.wv.most_similar(positive=items, negative=neg_items, topn = self.top_n)
        item_list = []

        for i in range(self.top_n):
            item_list.append(list(item_tuple[i]))

        ls1 = [self.df[self.df['bk'] == item_list[i][0]]['major'].values[0] for i in range(self.top_n)]
        maj = Counter(ls1).most_common(1)[0][0]
        ls2 = [self.df[self.df['bk'] == item_list[i][0]]['difficulty'].values[0] for i in range(self.top_n)]
        dif = np.mean(ls2)
        if user_grade == None:
            pass
        else:
            dif2 = user_grade
            dif = (dif + dif2)/2

        for i in range(self.top_n):
            if self.df[self.df['bk'] == item_list[i][0]]['difficulty'].values[0] == maj:
                pass
            else:
                item_list[i][1] = item_list[i][1] * 0.6

            if self.df[self.df['bk'] == item_list[i][0]]['difficulty'].values[0] - dif > 1:
                item_list[i][1] = item_list[i][1] * 0.9
            elif self.df[self.df['bk'] == item_list[i][0]]['difficulty'].values[0] - dif >= -0.2:
                item_list[i][1] = item_list[i][1] * 1.0
            elif self.df[self.df['bk'] == item_list[i][0]]['difficulty'].values[0] - dif >= -1:
                item_list[i][1] = item_list[i][1] * 0.6
            else: # if rec book is easier
                item_list[i][1] = item_list[i][1] * 0.4

        final_list = np.array(sorted(item_list, key=lambda x: x[1], reverse=True))[:,0][:10].tolist()
 
        return final_list



