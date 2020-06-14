from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
import os
from django.conf import settings


# Custom User
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    uname = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True)
    gender = models.IntegerField(default=0)
    major = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20, null=True)
    is_active = models.BooleanField('active', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['uname', 'gender', 'major']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# DB Models
class Product(models.Model):
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    buyer_id = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    complete_date = models.DateTimeField(blank=True, null=True)
    pname = models.CharField(max_length=50)
    category = models.IntegerField(default=10)
    price = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    p_status = models.IntegerField(default=0)
    image = models.FileField(upload_to='media', default='media/calculus.jpg')

    def __str__(self):
        return self.pname


class Post(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    reg_date = models.DateTimeField(default=timezone.now)
    hits = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    locker_check = models.IntegerField(default=0)

    @property
    def update_hits(self):
        self.hits += 1
        self.save()
        return

    def __str__(self):
        return self.title


class Schedule(models.Model):
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('course_id', 'user_id'),)

    def __str__(self):
        return f"{self.course_id}, {self.user_id}"


class Course(models.Model):
    c_number = models.CharField(max_length=20)
    cname = models.CharField(max_length=30)
    professor = models.CharField(max_length=20)

    first_time = models.CharField(max_length=20, default="")  # "13:30"
    second_time = models.CharField(max_length=20, null=True)  # "12:00"
    week = models.CharField(max_length=20, default="")  # "월,수"

    def __str__(self):
        return self.cname


class Locker(models.Model):
    l_number = models.CharField(max_length=20)
    status = models.IntegerField(default=0)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.l_number


class Book(models.Model):
    lec = models.CharField(max_length=40)
    prof = models.CharField(max_length=40)
    bk = models.CharField(max_length=40)
    publisher = models.CharField(max_length=40)
    author = models.CharField(max_length=40)
    serial = models.CharField(max_length=40)

    credit = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    major = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)

    book_img = models.FileField(upload_to='media', default='calculus.jpg')

    def __str__(self):
        return self.bk


class History(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    book_id = models.ForeignKey('Book', on_delete=models.CASCADE)

    def __str__(self):
        return f'user_id: {self.user_id}, book_id: {self.book_id}'



