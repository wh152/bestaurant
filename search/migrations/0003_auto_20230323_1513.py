# Generated by Django 2.1.5 on 2023-03-23 15:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_auto_20230323_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
