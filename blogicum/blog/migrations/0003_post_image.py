# Generated by Django 3.2.16 on 2024-05-12 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20240423_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(
                blank='True',
                upload_to='post_imagine',
                verbose_name='Изображение'),
        ),
    ]