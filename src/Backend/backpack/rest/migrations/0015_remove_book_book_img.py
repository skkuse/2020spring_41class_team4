# Generated by Django 3.0.6 on 2020-06-13 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0014_auto_20200613_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_img',
        ),
    ]
