from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseBadRequest
from rest.models import *
import os
from django.conf import settings


num_to_category = {'GEL': 0, 'CFT': 1, 'BIZ': 2, 'BUS': 3, 'ECO': 4, 'STA': 5,
     'GBA': 6, 'GEC': 7, 'PSY': 8, 'MAE': 9, 'ENG': 10, 'INT': 11, 'CAL': 12, 
     'ERC': 13, 'COV': 14, 'EEE': 15, 'EME': 16, 'ICE': 17, 'SWE': 18, 
     'ESM': 19, 'ECE': 20, 'EAM': 21, 'ECH': 22, 'IKS': 23, 'KLC': 24,
     'DKL': 25, 'GCC': 26, 'HFS': 27, 'GER': 28, 'RUS': 29, 'DSC': 30, 
     'LIS': 31, 'SWF': 32, 'PHL': 33, 'HIS': 34, 'CHI': 35, 'FRE': 36, 'EDU': 37, 
     'COM': 38, 'PAD': 39, 'PIL': 40, 'PSD': 41, 'GLD': 42, 'USS': 43, 'MCJ': 44, 
     'SOC': 45, 'CFS': 46, 'KID': 47, 'FBT': 48, 'IBT': 49, 'CHY': 50, 'AAI': 51, 
     'CNT': 52, 'SPT': 53, 'BIO': 54, 'ART': 55, 'COS': 56, 'MTH': 57, 'GED': 58, 
     'DBA': 59, 'CLA': 60, 'LIT': 61, 'ILI': 62, 'JAP': 63, 'CON': 64, 'EBM': 65}


@login_required
def main_page(request):
    return render(request, "main_page.html")

@login_required
def post_list(request):
    user_email = request.user
    user = User.objects.filter(email=user_email)
    uname = user[0].uname
    
    return render(request, "board_list.html", {'uname': uname})

@login_required
def post_detail(request, pk):
    products = Product.objects.filter(post_id=pk)
    seller = Post.objects.get(pk=pk).user_id

    id_list = list()
    for product in products:
        id_list.append(product.id)

    if request.user == seller:
        return render(request, "board_update.html")

    return render(request, "board_.html", {'pk': pk, 'products': id_list})

@login_required
def post_register(request):
    return render(request, "board_Register.html")

@login_required
def post_update(request, pk):
    return render(request, "board_update.html")



@login_required
def index(request):
    return render(request, "frontend/index.html")


@login_required
def search(request, search=None):
    return render(request, "frontend/transaction.html", { 'search': search })
    #return render(request, "frontend/search.html")


@login_required
def mypage(request):
    user_email = request.user
    user = User.objects.get(email=user_email)

    uname = user.uname
    major = user.major


    return render(request, "frontend/mypage.html", {'email': user_email, 'uname': uname, 'major': major})


@login_required
def transaction(request, search=None):
    return render(request, "frontend/transaction.html", { 'search': search })

@login_required
def product(request, pk):
    product = Product.objects.get(post_id=pk)
    post = Post.objects.get(pk=pk)
    seller_email = Post.objects.get(pk=pk).user_id

    # if request.user == seller_email:
    #    return render(request, "frontend/product_update.html")

    user_id = User.objects.get(email=seller_email)
    uname = user_id.uname
    pN = user_id.phone_number
    price = product.price
    category = product.category
    img = product.image.url
    pname = product.pname

    category_name = None
    for key, value in num_to_category.items():
        if category == value:
            category_name = key
    
    return render(request, "frontend/product.html", {'uname': uname, 'price': price, 'pN': pN, 
    'post_id': post.id, 'is_seller': user_id == request.user,
    'category': category_name, 'img': img, 'pname': pname, 'title': post.title, 'content': post.content})


@login_required
def product_update(request, pk=None):
    user = request.user
    data = {}
    data['uname'] = user.uname
    data['pN'] = user.phone_number
    if pk != None:
        post = Post.objects.get(pk=pk)
        data['is_update'] = True
        data['title'] = post.title
        data['content'] = post.content
        data['status'] = post.status
        data['locker_check'] = post.locker_check

        product = Product.objects.filter(post_id=pk)
        product = product[0]
        data['price'] = product.price
        data['pname'] = product.pname
        data['img_url'] = product.image.url
        data['post_id'] = pk
        data['product_id'] = product.id

    return render(request, "frontend/product_update.html", data)

@login_required
def upload_product(request):
    file = request.FILES.get('file')
    filename = request.POST.get('name')
    pname = request.POST.get('pname')
    price = request.POST.get('price')
    post_id = request.POST.get('post_id')
    product_id = request.POST.get('product_id')
    category = request.POST.get('category')

    if filename != '.':
        with open(os.path.join(settings.MEDIA_ROOT, filename), 'wb') as f:
            for line in file:
                f.write(line)

    if product_id != None:
        print(product_id)
        product = Product.objects.get(pk=product_id)
        product.pname = pname; product.category = category; product.price = price
        if filename != '.':
            product.image = filename
        product.save()
    else:
        post = Post.objects.get(pk=post_id)
        product = Product(pname=pname, category=category, price=price, post_id=post, image=filename)
        product.save()

    return HttpResponse("")

@login_required
def major_books(request):
    return render(request, "frontend/major_books.html")


@login_required
def recommendation(request):
    user_email = request.user
    user = User.objects.filter(email=user_email)
    uid = user[0].id

    return render(request, "frontend/recommended_books.html", {'user_id': uid})


@login_required
def schedule(request):
    user_email = request.user
    user = User.objects.get(email=user_email)

    schedules = Schedule.objects.filter(user_id=user.id)

    course_list = list()
    book_list = list()
    for schedule in schedules:
        course_list.append(schedule.course_id.id)
        cname = schedule.course_id.cname
        prof = schedule.course_id.professor
        book = Book.objects.filter(lec=cname, prof=prof)
        if len(book) == 0:
            book_list.append("")
        else:
            book_list.append(book[0].bk)
    
    print(book_list)

    return render(request, "schedule/index.html", {'course_list': course_list, 'book_list': book_list})

@login_required
def schedule_register(request, pk=None):
    if pk == None:
        return render(request, "frontend/schedule_register.html")
    else:
        user = request.user
        course = Course.objects.get(pk=pk)
        schedule = Schedule(user_id=user, course_id=course)
        try:
            schedule.save()
        except:
            return HttpResponseBadRequest("이미 등록된 유저입니다!")
        return HttpResponse("OK")

#def search(request):
#    return render(request, "search.html")


def schedule_workout(request):
    return render(request, "schedule/event-rowing-workout.html")