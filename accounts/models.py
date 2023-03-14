from django.db import models
from django.contrib.auth.models import User
from search.models import *
from django.db.models import Avg


# Can't have the same name as the built-in model User 
class UserAccount(models.Model):
    # User gives an id, email, username, password and other irrelevent fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, primary_key=True)
    restaurantOwner = models.BooleanField(default=False)
    about = models.CharField(max_length=1024, blank=True)
    photo = models.ImageField(upload_to='profile_images', null=True, blank=True)
    # To reference a model not yet defined you must put its name as a string
    #recentlyReviewed = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Restaurant(models.Model):
    restaurantID = models.AutoField(primary_key=True)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    restaurantName = models.CharField(max_length=128, unique=True)
    category = models.CharField(max_length=128)
    address = models.CharField(max_length=256, unique=True)
    logo = models.ImageField(upload_to='restaurant_logos', null=True, blank=True)
    averageRating = models.FloatField(null=True, blank=True)
    dateAddedd = models.DateField(null=False)

    def __str__(self):
        return str(self.restaurantID) + ': ' + self.restaurantName
    
    def average_rating(self) -> float:
        return Review.objects.filter(restaurant=self).aggregate(Avg("rating"))["rating__avg"] or 0


class Advertisement(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, primary_key=True)
    description = models.CharField(max_length=1024)
    advertImage = models.ImageField(upload_to='advertisement_images')

    def __str__(self):
        return self.restaurant.restaurantName + ': ' + self.description
