# Generated by Django 2.2.28 on 2023-03-03 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20230303_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='averageRating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='restaurantName',
            field=models.CharField(max_length=128, unique=True, verbose_name='Restaurant name'),
        ),
    ]
