from django import forms
from accounts.models import *
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'username', 'password',)


class UserAccountForm(forms.ModelForm):

    about = forms.CharField(max_length=1024, help_text="Enter a bit about yourself", required = False)

    class Meta:
        model = UserAccount
        fields = ('photo','about')


class RestaurantRegistrationForm(forms.ModelForm):
    restaurantName = forms.CharField(max_length=128, label="Restaurant name", help_text="Enter your restaurant name",)
    category = forms.CharField(max_length = 128, help_text = "What category is your restaurant? E.g. Fast food, fine dining, etc")
    address = forms.CharField(max_length = 256, help_text = "Enter the address of your restaurant" )

    class Meta:
        model = Restaurant
        fields = ('restaurantName', 'category', 'address','logo')



class LoginForm (forms.Form):
    username_or_email = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


