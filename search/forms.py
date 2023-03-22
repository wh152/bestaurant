from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator 

from accounts.models import *
from .models import *


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    comment = forms.CharField(max_length=1024)
    
    class Meta:
        model = Review
        fields = ('rating', 'comment')
