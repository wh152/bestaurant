from accounts.models import *
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def viewOwnRestaurants(request):
    if request.user.is_anonymous:
        return HttpResponse("You are not logged in.")
    user = User.objects.get(username=request.user.username)
    userAccount = UserAccount.objects.get(user=user)
    if not userAccount.restaurantOwner:
        return HttpResponse("You are not a restaurant owner.")
    restaurants = [restaurant for restaurant in Restaurant.objects.filter(owner=userAccount)]
    context = {}
    for restaurant in restaurants:
        context[restaurant.restaurantName] = {
            "category": restaurant.category,
            "address": restaurant.address,
            "logo": restaurant.logo,
            "averageRating": restaurant.averageRating
        }
    return render(request, 'managerestaurants/all_owned_restaurants.html', context=context)
