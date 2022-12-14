# Generated by Django 4.1.2 on 2022-11-14 05:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfume_shop', '0045_perfume_image2_alter_perfumebottle_discount_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PerfumeDescription',
            new_name='Detail',
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='discount',
            field=models.PositiveIntegerField(default=47),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='price',
            field=models.FloatField(default=16025858.87, validators=[django.core.validators.MinValueValidator(1000000)]),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='quantity',
            field=models.PositiveIntegerField(default=487),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='rate',
            field=models.FloatField(default=0.1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='size',
            field=models.FloatField(default=991.47, validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(1000)]),
        ),
    ]
