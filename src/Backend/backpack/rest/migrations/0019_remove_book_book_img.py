# Generated by Django 3.0.6 on 2020-06-13 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0018_book_book_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_img',
        ),
    ]
