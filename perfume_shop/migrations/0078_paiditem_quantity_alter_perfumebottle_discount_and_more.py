# Generated by Django 4.1.2 on 2022-11-28 15:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfume_shop', '0077_alter_perfumebottle_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paiditem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='discount',
            field=models.PositiveIntegerField(default=14),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='price',
            field=models.FloatField(default=7213740.83, validators=[django.core.validators.MinValueValidator(1000000)]),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='quantity',
            field=models.PositiveIntegerField(default=119),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='rate',
            field=models.FloatField(default=1.71, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='size',
            field=models.FloatField(default=236.19, validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(1000)]),
        ),
    ]