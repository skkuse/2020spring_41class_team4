# Generated by Django 3.0.6 on 2020-06-13 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0023_book_book_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.FileField(default='media/calculus.jpg', upload_to='media'),
        ),
    ]
