# Generated by Django 4.1.2 on 2022-11-09 15:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfume_shop', '0042_alter_perfumebottle_discount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfumebottle',
            name='discount',
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='price',
            field=models.FloatField(default=10944927.73, validators=[django.core.validators.MinValueValidator(1000000)]),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='quantity',
            field=models.PositiveIntegerField(default=637),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='rate',
            field=models.FloatField(default=0.4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='size',
            field=models.FloatField(default=986.68, validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(1000)]),
        ),
    ]
