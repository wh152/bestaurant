# Generated by Django 2.1.5 on 2023-02-27 10:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('restaurantID', models.AutoField(primary_key=True, serialize=False)),
                ('restaurantName', models.CharField(max_length=128, unique=True)),
                ('category', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=256, unique=True)),
                ('logo', models.ImageField(blank=True, upload_to='restaurant_logos')),
                ('averageRating', models.FloatField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('restaurantOwner', models.BooleanField(default=False)),
                ('about', models.CharField(blank=True, max_length=1024)),
                ('photo', models.ImageField(blank=True, upload_to='profile_images')),
            ],
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('restaurant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.Restaurant')),
                ('description', models.CharField(max_length=1024)),
                ('advertImage', models.ImageField(upload_to='advertisement_images')),
            ],
        ),
        migrations.AddField(
            model_name='useraccount',
            name='recentlyReviewed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Restaurant'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.UserAccount'),
        ),
    ]