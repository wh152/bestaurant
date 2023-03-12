from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator 

from accounts.models import *
from .models import *


class ReviewForm(forms.ModelForm):
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    comment = models.CharField(max_length=1024)
    
    class Meta:
        model = Review
        fields = ('rating', 'comment')
