# Generated by Django 4.1.2 on 2022-11-02 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfume_shop', '0012_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfume',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='perfume_shop.brand'),
        ),
    ]
