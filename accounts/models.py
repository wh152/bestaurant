from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.template.defaultfilters import slugify

import search


class UserAccount(models.Model):
    # User gives an id, email, username, password and other fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, primary_key=True)
    username_slug = models.SlugField(unique=True)
    restaurantOwner = models.BooleanField(default=False)
    about = models.CharField(max_length=1024, blank=True)
    photo = models.ImageField(upload_to='profile_images', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # slug must be set in save() manually
        self.username_slug = slugify(self.user.username)
        super(UserAccount, self).save(*args, **kwargs)


class Restaurant(models.Model):
    restaurantID = models.AutoField(primary_key=True)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    restaurantName = models.CharField(max_length=128, unique=True)
    restaurantNameSlugged = models.SlugField(unique=True)
    category = models.CharField(max_length=128)
    address = models.CharField(max_length=256, unique=True)
    logo = models.ImageField(upload_to='restaurant_logos', null=True, blank=True)
    averageRating = models.FloatField(null=True, blank=True)
    # automatically adds the date of the object's creation
    dateAdded = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.restaurantID) + ': ' + self.restaurantName

    def save(self, *args, **kwargs):
        self.restaurantNameSlugged = slugify(self.restaurantName)
        super(Restaurant, self).save(*args, **kwargs)
    
    def average_rating(self) -> float:
        # calculates average rating of a Restaurant object
        return search.models.Review.objects.filter(restaurant=self).aggregate(Avg("rating"))["rating__avg"] or 0


class Advertisement(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, primary_key=True)
    description = models.CharField(max_length=1024)
    advertImage = models.ImageField(upload_to='advertisement_images')

    def __str__(self):
        return self.restaurant.restaurantName + ': ' + self.description
