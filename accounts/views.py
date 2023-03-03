from django.shortcuts import render
from accounts.forms import RegistrationForm, UserAccountForm, RestaurantRegistrationForm

# Create your views here.

def register(request):
    registrationSuccess = False

    if request.method == 'POST':
        #attempt to grab information from the raw form information. 
        customer_form = RegistrationForm(request.POST)
        user_account_form = UserAccountForm(request.POST)
        restaurant_owner_form = RestaurantRegistrationForm(request.POST)

        #If the two forms are valid save the user's form data to the database
        if customer_form.is_valid() and user_account_form.is_valid():
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
                print(user_account)
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
    return render(request, 'bestaurant/register.html', context = {'user_form': customer_form, 'user_account_form':user_account_form, 'profile_form': restaurant_owner_form, 'registered': registrationSuccess})
