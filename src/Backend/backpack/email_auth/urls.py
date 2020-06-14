from django.urls import path

from email_auth import views
from django.contrib.auth.views import LogoutView

app_name = 'email_auth'


urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name="register"),
    path('verify/<email>/<token>', views.UserVerificationView.as_view(), name="verify"),
    path('login/', views.UserLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]