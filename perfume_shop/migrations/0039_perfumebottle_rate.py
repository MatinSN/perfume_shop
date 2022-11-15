# Generated by Django 4.1.2 on 2022-11-09 15:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfume_shop', '0038_remove_perfumebottle_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfumebottle',
            name='rate',
            field=models.FloatField(default=1.55, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]