# Generated by Django 3.0.6 on 2020-06-13 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0024_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_img',
        ),
    ]