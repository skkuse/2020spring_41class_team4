# Generated by Django 3.0.6 on 2020-06-14 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0030_auto_20200613_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='locker_check',
            field=models.IntegerField(default=0),
        ),
    ]
