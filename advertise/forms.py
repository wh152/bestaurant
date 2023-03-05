from django import forms
from accounts.models import *

class AdvertisementForm(forms.ModelForm):
    description = forms.CharField(max_length=1024, help_text="Advertisement description")
    advertImage = forms.ImageField()

    class Meta:
        model = Advertisement
        exclude = ('restaurant',)