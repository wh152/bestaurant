from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.models import *
from accounts.forms import AdvertiseForm


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
    return render(request, 'other/all_owned_restaurants.html', context=context)


def viewAllUsers(request):
    return render(request, 'other/all_users.html', context={"users": UserAccount.objects.all()})


def viewOneUser(request, username):
    try:
        user = User.objects.get(username=username)
        userAccount = UserAccount.objects.get(user=user)
        context = {}
        context["username"] = user.username
        context["usernameJoined"] = user.username.replace(" ", "_")
        context["restaurantOwner"] = userAccount.restaurantOwner
        context["about"] = userAccount.about if len(userAccount.about) > 0 else None
        context["photo"] = userAccount.photo
        context["recentlyReviewed"] = userAccount.recentlyReviewed
        context["sluggedNames"] = []
        if userAccount.restaurantOwner:
            owned = Restaurant.objects.filter(owner=userAccount)
            # include the restaurant names with underscores for URL compatibility
            restaurants = [(r, r.restaurantName.replace(" ", "_")) for r in owned]
            context["restaurants"] = restaurants if len(restaurants) > 0 else None
        else:
            context["restaurants"] = None
        print("context", context)
        return render(request, 'other/one_user.html', context=context)
    except User.DoesNotExist:
        return HttpResponse("Requested user does not exist")


@login_required
def advertise(request):
    try:
        userAccount = UserAccount.objects.get(user=request.user)
        if not userAccount.restaurantOwner:
            return HttpResponse("You are not a restaurant owner.")
        if request.method == "POST":
            form = AdvertiseForm(request.POST, user=request.user)
            if form.is_valid():
                restaurant = request.post["restaurant"]
                description = request.post["description"]
                advertImage = request.post["advertImage"]
                advertisement = Advertisement.objects.create(
                    restaurant=restaurant, description=description, advertImage=advertImage
                )
                advertisement.save()
                return HttpResponseRedirect("/advertise/success")
            else:
                return render("other/make_advert.html", {"form": form})
        else:
            form = AdvertiseForm(user=request.user)
            return render("other/create_advert.html", {"form": form})
    except:
        return HttpResponse("You must log in to see this page.")


def temp(request):
    return HttpResponse("At least it's not a 404")
