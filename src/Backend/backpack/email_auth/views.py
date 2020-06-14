from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status
from rest_framework.response import Response

from backpack import settings
from rest.models import *
from email_auth.serializers import RegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    Register a new user.
    """
    
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = RegistrationSerializer
    template_name = 'email_auth/user_model.html'

    def get(self, request):
        serializer = RegistrationSerializer
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('/email_auth/login')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class UserVerificationView(TemplateView):
    """
    Verify a user
    """
    
    model = User
    redirected_url = '/email_auth/login/'
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            messages.info(request, '인증이 완료되었습니다.')
        else:
            messages.error(request, '인증이 실패되었습니다.')
        return HttpResponseRedirect(self.redirected_url)

    def is_valid_token(self, **kwargs):
        email = kwargs.get('email')
        token = kwargs.get('token')
        user = self.model.objects.get(email=email)
        is_valid = self.token_generator.check_token(user, token)
        if is_valid:
            user.is_active = True
            user.save()
        return is_valid

    
class UserLoginView(LoginView):
    """
    Log in
    """

    template_name = 'email_auth/login_form.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)
