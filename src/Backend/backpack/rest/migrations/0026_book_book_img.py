# Generated by Django 3.0.6 on 2020-06-13 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0025_remove_book_book_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_img',
            field=models.FileField(default='calculus.jpg', upload_to='media'),
        ),
    ]