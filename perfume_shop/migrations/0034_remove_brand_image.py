# Generated by Django 4.1.2 on 2022-11-09 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfume_shop', '0033_brand_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='image',
        ),
    ]
