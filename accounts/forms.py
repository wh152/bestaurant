from django import forms
from accounts.models import *
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(att))