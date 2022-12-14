# Generated by Django 4.1.2 on 2022-11-09 15:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfume_shop', '0039_perfumebottle_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfumebottle',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='perfumebottle',
            name='price',
        ),
        migrations.RemoveField(
            model_name='perfumebottle',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='perfumebottle',
            name='size',
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='rate',
            field=models.FloatField(default=0.9, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
