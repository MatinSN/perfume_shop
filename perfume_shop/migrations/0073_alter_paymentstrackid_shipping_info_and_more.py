# Generated by Django 4.1.2 on 2022-11-27 18:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfume_shop', '0072_alter_paymentstrackid_shipping_info_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentstrackid',
            name='shipping_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='perfume_shop.address'),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='discount',
            field=models.PositiveIntegerField(default=17),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='price',
            field=models.FloatField(default=19127318.63, validators=[django.core.validators.MinValueValidator(1000000)]),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='quantity',
            field=models.PositiveIntegerField(default=684),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='rate',
            field=models.FloatField(default=0.69, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='size',
            field=models.FloatField(default=747.2, validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(1000)]),
        ),
    ]
