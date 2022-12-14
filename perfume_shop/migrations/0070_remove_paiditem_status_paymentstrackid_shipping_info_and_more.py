# Generated by Django 4.1.2 on 2022-11-27 18:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfume_shop', '0069_remove_rating_comment_remove_rating_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paiditem',
            name='status',
        ),
        migrations.AddField(
            model_name='paymentstrackid',
            name='shipping_info',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='perfume_shop.address'),
        ),
        migrations.AddField(
            model_name='paymentstrackid',
            name='status',
            field=models.CharField(choices=[('Not Paid', 'Not Paid'), ('Processing', 'Processing'), ('Sent', 'Send'), ('Received', 'Received')], default=None, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='discount',
            field=models.PositiveIntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='price',
            field=models.FloatField(default=18666763.59, validators=[django.core.validators.MinValueValidator(1000000)]),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='quantity',
            field=models.PositiveIntegerField(default=286),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='rate',
            field=models.FloatField(default=2.72, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='perfumebottle',
            name='size',
            field=models.FloatField(default=894.23, validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(1000)]),
        ),
    ]
