from django.contrib.auth import password_validation, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest.models import User
from backpack import settings
from email_auth.utils import send_verification_email


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta(object):
        extra_kwargs = {
            "password": {
                "style": {"input_type": "password"},
                "write_only": True,
            }
        }
        model = User
        fields = ('uname', 'email', 'password', 'major', 'phone_number')

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)

        user.email = email

        email_query = User.objects.filter(email=email)

        if email_query.exists():
            raise ValidationError('The user already signed up')
        else:
            user.save()
            send_verification_email(user)
        
        return user

    def validate_email(self, email):
        user, domail = email.rsplit("@", 1)

        return "@".join([user, domail.lower()])

    def validate_password(self, password):
        # password_validation.validate_password(password)

        return password

"""
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials")
"""