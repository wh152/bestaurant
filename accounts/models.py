from django.db import models
from django.contrib.auth.models import User


# Can't have the same name as the built-in model User 
class UserAccount(models.Model):
    # User gives an id, email, username, password and other irrelevent fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, primary_key=True)
    restaurantOwner = models.BooleanField(default=False)
    about = models.CharField(max_length=1024, blank=True)
    photo = models.ImageField(upload_to='profile_images', blank=True)
    # To reference a model not yet defined you must put its name as a string
    recentlyReviewed = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Restaurant(models.Model):
    restaurantID = models.AutoField(primary_key=True)
    owner = models.OneToOneField(UserAccount, on_delete=models.SET_NULL, null=True)
    restaurantName = models.CharField(max_length=128, unique=True)
    category = models.CharField(max_length=128)
    address = models.CharField(max_length=256, unique=True)
    logo = models.ImageField(upload_to='restaurant_logos', blank=True)
    averageRating = models.FloatField(blank=True)

    def __str__(self):
        return str(self.restaurantID) + ': ' + self.restaurantName


class Advertisement(models.Model):
    # find a workaround to avoid delete restaurants when their ad is deleted
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, primary_key=True)
    description = models.CharField(max_length=1024)
    advertImage = models.ImageField(upload_to='advertisement_images')

    def __str__(self):
        return self.restaurant.restaurantName + ': ' + self.description
