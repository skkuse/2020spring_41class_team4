from django.shortcuts import render
from rest_framework import viewsets, views
from .serializers import *
from .models import *
from rest_framework.response import Response
from django.http import HttpResponseForbidden
from django_filters import rest_framework as filters
from .filters import *


class UserViewSet(viewsets.ModelViewSet):
    """
    If you want change each REST API personally,
    def list(self, request):
            pass

        def create(self, request):
            pass

        def retrieve(self, request, pk=None):
            pass

        def update(self, request, pk=None):
            pass

        def partial_update(self, request, pk=None):
            pass

        def destroy(self, request, pk=None):
            pass
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ('email', 'uname', 'gender', 'major')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ('id','post_id', 'pname', 'category')

    def create(self, request):
        pname = request.POST.get('pname')
        post_id = request.POST.get('post_id')
        price = request.POST.get('price')
        post = Post.objects.get(pk=post_id)
        category = request.POST.get('category')
        
        product = Product(pname=pname, price=price, post_id=post, category=category)
        product.save()
        return Response("OK")
    
    def update(self, request, pk=None):
        pname = request.data.get('pname')
        post_id = request.data.get('post_id')
        price = request.data.get('price')
        category = request.data.get('category')
        image = request.data.get('image')
        product = Product.objects.get(pk=pk)
        user_id = product.post_id.user_id

        if user_id != request.user:
            return HttpResponseForbidden()

        product.pname = pname; product.price = price; product.category = category; product.image = image
        product.save()
        return Response("OK")


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter

    def create(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        user_id = request.user
        locker_check = request.POST.get('locker_check')
        
        post = Post(title=title, content=content, user_id=user_id, locker_check=locker_check)
        post.save()
        return Response(post.id)

    def update(self, request, pk=None):
        title = request.data.get('title')
        content = request.data.get('content')
        status = request.data.get('status')
        locker_check = request.data.get('locker_check')
        user_id = request.user

        if user_id != request.user:
            return HttpResponseForbidden()

        post = Post.objects.get(pk=pk)
        post.title = title; post.content = content; post.status = status; post.locker_check = locker_check
        
        post.save()
        return Response(post.id)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filterset_fields = ('id', 'user_id', 'course_id')


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_fields = ('id', 'c_number', 'cname', 'professor')


class LockerViewSet(viewsets.ModelViewSet):
    queryset = Locker.objects.all()
    serializer_class = LockerSerializer
    filterset_fields = ('id', 'status', 'l_number')

