# Generated by Django 4.1.2 on 2022-11-09 15:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfume_shop', '0036_remove_perfumebottle_rate_perfumebottle_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfumebottle',
            name='rate',
            field=models.FloatField(default=4.930762828796311, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]