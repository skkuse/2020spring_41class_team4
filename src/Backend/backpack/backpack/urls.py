"""backpack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from . import views
from django.conf import settings
from django.conf.urls.static import static


schema_url_v1_patterns = [
    url(r'^rest/', include('rest.urls')),
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Restful API",
        default_version='v1',
        description="안녕하세요. Backpack 서비스 Open API 문서 페이지 입니다.",
        contact=openapi.Contact(email="sweteam4@google.com"),
        license=openapi.License(name="backpack"),
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_v1_patterns,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest/', include('rest.urls')),
    path('email_auth/', include('email_auth.urls')),
    # path('main/', views.main_page),
    path('recommend/', include('recommendation.urls')),

    # frontend urls
    path('home/', views.index),
    path('home/search/', views.search),
    path('home/mypage/', views.mypage),
    path('home/major_books/', views.major_books),
    path('home/recommendation/', views.recommendation),
    path('home/transaction/', views.transaction),
    path('home/transaction/<search>/', views.transaction),
    path('home/product/<int:pk>/', views.product),
    path('home/product/update/<int:pk>/', views.product_update),
    path('home/product/register/', views.product_update),
    path('upload_product/', views.upload_product),
    path('home/search/', views.search),
    path('home/schedule/', views.schedule),
    path('home/schedule/register/', views.schedule_register),
    path('home/schedule/register/<int:pk>/', views.schedule_register),

    path('home/schedule/workout/', views.schedule_workout),



    path('post/', views.post_list),
    path('post/detail/<pk>/', views.post_detail),
    path('post/update/<pk>/', views.post_update),
    path('post/register/', views.post_register),

    url(r'^swagger(?P<format>\.json|\.yaml)/$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]


urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)