from django.db import models
from accounts.models import *


class Review(models.Model):
    reviewID = models.AutoField(primary_key=True)
    reviewer = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.CharField(max_length=1024)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return ' - '.join([str(self.reviewID), self.restaurant.restaurantName, self.reviewer.user.username, 
                            str(self.rating), self.comment])
