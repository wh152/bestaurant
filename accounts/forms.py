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
    categoryChoices = (
        ("Casual Dining", "Casual Dining"),
        ("Fine Dining", "Fine Dining"),
        ("Fast Food", "Fast Food"),
        ("Cafe", "Cafe"),
        ("Coffeehouse", "Coffeehouse")
    )
    restaurantName = forms.CharField(max_length=128, label="Restaurant name", help_text="Enter your restaurant name",)
    category = forms.ChoiceField(widget=forms.RadioSelect, choices=categoryChoices)
    address = forms.CharField(max_length = 256, help_text = "Enter the address of your restaurant" )

    class Meta:
        model = Restaurant
        fields = ('restaurantName', 'category', 'address','logo')



class LoginForm (forms.Form):
    username_or_email = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class AdvertiseForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(AdvertiseForm, self).__init__(*args, **kwargs)
        restaurantsOwned = Restaurant.objects.filter(owner=user)
        notAdvertised = []
        for restaurant in restaurantsOwned:
            if not Advertisement.objects.filter(restaurant=restaurant):
                notAdvertised.append((restaurant, restaurant.restaurantName))
        self.fields["restaurant"] = forms.ChoiceField(
            widget=forms.RadioSelect, choices=notAdvertised
        )
        self.fields["description"] = forms.CharField(
            max_length=1024, label="Advert text", help_text="Sell you brand!"
        )
        self.fields["advertImage"] = forms.ImageField()
    class Meta:
        model = Advertisement
        fields = ('description', 'advertImage')
