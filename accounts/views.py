from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, UserAccountForm, RestaurantRegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import *

# Create your views here.

def register(request):
    registrationSuccess = False

    if request.method == 'POST':
        #attempt to grab information from the raw form information. 
        customer_form = RegistrationForm(request.POST)
        user_account_form = UserAccountForm(request.POST)
        restaurant_owner_form = RestaurantRegistrationForm(request.POST)

        #If the two forms are valid save the user's form data to the database
        if customer_form.is_valid() and user_account_form.is_valid() and customer_form.cleaned_data['password'] == customer_form.cleaned_data['confirm_password']:
            #save the users form data to the database.
            customer = customer_form.save()

            #hash password with the set_password method. Once hashed, we can update the user object.
            customer.set_password(customer.password)
           
            customer.save()
            user_account = user_account_form.save(commit=False)

            user_account.user = customer

            if 'photo' in request.FILES:
                user_account.photo = request.FILES['photo']

            user_account.save()

            if restaurant_owner_form.is_valid():
                #set commit to false to avoid integrity problems
                restaurant = restaurant_owner_form.save(commit=False)
                restaurant.owner = user_account

                #if the user provided a profile picture, we need to get it from the input form and put it in 
                #the UserAccount model.
                if 'logo' in request.FILES:
                    restaurant.logo = request.FILES['logo']

                #save the restaurant model instance
                restaurant.save()


            #update variable to indicate that the template registration was successful
            registrationSuccess = True

        else:
            #invalid form or forms - mistakes or something else. Print problems to the terminal
            print(customer_form.errors, user_account_form.errors, restaurant_owner_form.errors)
    else:
        #not an HTTP POST, so we render our form using two ModelForm instances. These forms will be
        #blank, ready for user input.
        customer_form = RegistrationForm()
        user_account_form = UserAccountForm()
        restaurant_owner_form = RestaurantRegistrationForm()

    #render the template depending on the context.
    return render(request, 'registration/registration_form.html', context = {'user_form': customer_form, 'user_account_form':user_account_form, 'profile_form': restaurant_owner_form, 'registered': registrationSuccess})


def login(request):
    loginSuccess = False
    loginFailed = False
    if request.method == 'POST':
        login_form= LoginForm(request.POST)

        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        #use Django's machinery to try to see if the username/password combination is valid - if it is, a User object 
        #is returned.

        #filter objects first by username, if an object is returned check if password matches. If an empty query set is returned, filter 
        # by email, email is not unique so if a non empty query set is returned loop over each object and see if password matches for any. 
        
        
        try:
            #try to get the user with the given email, if nothing is returned we go to the except block
            user_object = User.objects.get(username = username_or_email)

            if check_password(password, user_object.password):
                loginSuccess = True
        except:
            #it is possible for more than one user to have the same email, so we use filter and loop over 
            #all the objects returned and see if there is a password match
            user_objects = User.objects.filter(email = username_or_email)
            for current_user in user_objects:
                if check_password(password, current_user.password):
                    loginSuccess = True
                    break
        
        if not loginSuccess:
            loginFailed = True

    else:
        login_form = LoginForm()

    return render(request, 'registration/login.html', context = {'login_form': login_form, 'logged_in': loginSuccess, 'login_failed' : loginFailed})


@login_required
def logout(request):
    logout(request)
    return redirect('accounts: logout')


