from django.shortcuts import render, redirect
from accounts.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse
from .models import *
from django.conf import settings


def registrationClosed(request):

    return render(request, 'registration/registration_closed.html')


def register(request):

    if not settings.REGISTRATION_OPEN:
        return redirect('registrationClosed')
    if request.user.is_authenticated:
        return redirect(reverse('other:index'))
    registrationSuccess = False
    registrationFormValid = True

    if request.method == 'POST':
        #attempt to grab information from the raw form information. 
        customer_form = RegistrationForm(request.POST)
        user_account_form = UserAccountForm(request.POST)
        is_restaurant_owner_form = RegistrationRestaurantOwnerForm(request.POST)

        #If the two forms are valid save the user's form data to the database
        if customer_form.is_valid() and user_account_form.is_valid() and is_restaurant_owner_form.is_valid() and customer_form.cleaned_data['password'] == customer_form.cleaned_data['confirm_password']:
            #save the users form data to the database.
            customer = customer_form.save()

            #hash password with the set_password method. Once hashed, we can update the user object.
            customer.set_password(customer.password)
           
            customer.save()
            user_account = user_account_form.save(commit=False)

            user_account.user = customer

            if 'photo' in request.FILES:
                photo_extension = request.FILES['photo']._name.split(".")[-1]
                request.FILES['photo']._name = ".".join([slugify(user_account.user.username), photo_extension])
                user_account.photo = request.FILES['photo']
            
            user_account.restaurantOwner = is_restaurant_owner_form.cleaned_data['restaurantOwner']

            user_account.save()

            #update variable to indicate that the template registration was successful
            login(request, customer, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(reverse('other:index'))

        else:
            #invalid form or forms - mistakes or something else. Print problems to the terminal
            registrationFormValid = False
            print(customer_form.errors, user_account_form.errors)
    else:
        #not an HTTP POST, so we render our form using two ModelForm instances. These forms will be
        #blank, ready for user input.
        customer_form = RegistrationForm()
        user_account_form = UserAccountForm()
        is_restaurant_owner_form = RegistrationRestaurantOwnerForm()

    #render the template depending on the context.
    return render(request, 'registration/registration_form.html', context = {
        'user_form': customer_form, 
        'user_account_form':user_account_form, 
        'is_restaurant_owner_form': is_restaurant_owner_form,
        'registered': registrationSuccess,
        'form_valid': registrationFormValid
    })


def user_login(request):

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
                    user_object = current_user
                    loginSuccess = True
                    break
        
        if not loginSuccess:
            loginFailed = True

        if loginSuccess:
            if not user_object.is_active:
                return render(reverse('other:index'))
            else:
                login(request, user_object, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('other:index')
        else:
            # if the credentials entered are not a match give the user the form again
            login_form = LoginForm()
    else:
        login_form = LoginForm()
       

    return render(request, 'registration/login.html', context = {'login_form': login_form, 'logged_in': loginSuccess, 'login_failed': loginFailed})


@login_required
def change_description(request):

    if request.method == 'POST':
        form = ChangeDescriptionForm(request.POST)
        if form.is_valid():
            try:
                user_account = UserAccount.objects.get(user=request.user)
                user_account.about = request.POST.get('about')
                user_account.save()
                return redirect(reverse('other:viewOneUser', kwargs={
                    "username_slug": user_account.username_slug
                }))
            except User.DoesNotExist:
                return render(request, 'account/login.html')
        else:
            print("form.errors", form.errors)
            return render(request, "other/change_description.html", {'form': form, 'errors': form.errors})

    else:
        form = ChangeDescriptionForm()
        return render(request, 'other/change_description.html', {'form': form, 'errors': None})


@login_required
def change_image(request):
    if request.method == 'POST':
        form = ChangeImageForm(request.POST, request.FILES)
        user_account = UserAccount.objects.get(user=request.user)
        if form.is_valid() and form.changed_data:
            user_account.photo.delete(save=False)
            user_account.photo.save(user_account.username_slug + ".jpg", request.FILES['photo'])
            return redirect(reverse('other:viewOneUser', kwargs={
            "username_slug": user_account.username_slug
        }))
        else:
            return redirect(reverse('other:change_image'))

    else:
        form = ChangeImageForm()
        return render(request, 'other/change_image.html', {'form': form})
