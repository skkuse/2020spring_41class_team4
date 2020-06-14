from django.urls import path, include
from django.conf.urls import url
from .views import *



urlpatterns = [
    path('item/', rec_item.as_view(), name="Recommend Item"),
    path('user/', rec_user_item.as_view(), name="Recommend User")
]

