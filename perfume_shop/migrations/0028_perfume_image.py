# Generated by Django 4.1.2 on 2022-11-09 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfume_shop', '0027_remove_perfume_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfume',
            name='image',
            field=models.ImageField(default='p1.jpg', upload_to='perfumes'),
        ),
    ]