from django.db import models
from accounts.models import Restaurant

class Review(models.Model):
    restaurantID = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

#Base review model for foreign key field
