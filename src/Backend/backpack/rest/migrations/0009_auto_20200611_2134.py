# Generated by Django 3.0.6 on 2020-06-11 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0008_auto_20200605_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='buyer_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
