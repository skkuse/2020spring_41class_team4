from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from email_utils import send_email

from backpack import settings

def send_verification_email(user):
    token = default_token_generator.make_token(user)
    url = build_verification_link(user, token)
    send_email(
        subject='회원가입을 축하드립니다.',
        context={
            'url': url
        },
        recipient_list=[user.email],
        from_email=settings.EMAIL_HOST_USER,
        template_name='email_auth/verify_email_template'
    )

def build_verification_link(user, token):
    return 'http://34.64.191.230:8000/email_auth/verify/{}/{}'.format(user.email, token)
