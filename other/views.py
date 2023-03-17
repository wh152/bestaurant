from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from accounts.models import *
from accounts.forms import AdvertiseForm, RestaurantForm
from search.forms import *

def index(request):
    return render(request, 'index.html')


@login_required
def viewOwnRestaurants(request):
    if request.user.is_anonymous:
        return HttpResponse("You are not logged in.")
    user = User.objects.get(username=request.user.username)
    userAccount = UserAccount.objects.get(user=user)
    if not userAccount.restaurantOwner:
        return HttpResponse("You are not a restaurant owner.")
    context = {"restaurants": {}}
    for restaurant in Restaurant.objects.filter(owner=userAccount):
        context["restaurants"][restaurant] = {
            "restaurantName": restaurant.restaurantName,
            "category": restaurant.category,
            "address": restaurant.address,
            "logo_path": restaurant.logo.__str__() if restaurant.logo else None,
            "averageRating": restaurant.averageRating
        }
    return render(request, 'other/all_owned_restaurants.html', context=context)


def viewAllUsers(request):
    return render(request, 'other/all_users.html', context={"users": UserAccount.objects.all()})


def viewOneUser(request, username_slug):
    try:
        user_account = UserAccount.objects.get(username_slug=username_slug)
        context = {}
        context["username"] = user_account.user.username
        context["restaurantOwner"] = user_account.restaurantOwner
        context["about"] = user_account.about if len(user_account.about) > 0 else None
        context["photo"] = user_account.photo
        if context["photo"]:
            context["photo_path"] = context["photo"].__str__() 
        else:
            context["photo_path"] = "profile_images/default.jpg"
        context["recentlyReviewed"] = user_account.recentlyReviewed
        if user_account.restaurantOwner:
            owned = Restaurant.objects.filter(owner=user_account)
            # include the restaurant names with underscores for URL compatibility
            restaurants = [(r, r.restaurantNameSlugged) for r in owned]
            context["restaurants"] = restaurants if len(restaurants) > 0 else None
        else:
            context["restaurants"] = None
        return render(request, 'other/one_user.html', context=context)
    except User.DoesNotExist:
        return HttpResponse("Requested user does not exist")


@login_required
def advertise(request):
    userAccount = UserAccount.objects.get(user=request.user)
    if not userAccount.restaurantOwner:
        return HttpResponse("You are not a restaurant owner.")
    restaurantsOwned = Restaurant.objects.filter(owner=userAccount)
    notAdvertised = []
    for restaurant in restaurantsOwned:
        if not Advertisement.objects.filter(restaurant=restaurant):
            notAdvertised.append((restaurant.restaurantID, restaurant.restaurantName))
    if len(notAdvertised) == 0:
        return HttpResponse("All your restaurants already have advertisements")
    if request.method == "POST":
        form = AdvertiseForm(userAccount, request.POST, request.FILES)
        if form.is_valid():
            restaurant = Restaurant.objects.get(restaurantID=int(form.cleaned_data['restaurant']))
            description = form.cleaned_data['description']
            advertImage = request.FILES['advertImage']
            image_extension = request.FILES['advertImage']._name.split(".")[-1]
            request.FILES['advertImage']._name = ".".join([restaurant.restaurantNameSlugged, image_extension])
            Advertisement.objects.create(restaurant=restaurant, description=description, 
                                        advertImage=advertImage)
            return redirect(reverse('other:advertiseSuccess'))
        else:
            return render(request, "other/create_advertisement.html", {"form": form})
    else:
        form = AdvertiseForm(userAccount)
        return render(request, "other/create_advertisement.html", {"form": form})


@login_required
def advertiseSuccess(request):
    return render(request, 'other/advert_success.html')


@login_required
def addRestaurant(request):
    userAccount = UserAccount.objects.get(user=request.user)
    if not userAccount.restaurantOwner:
        return HttpResponse("You are not a restaurant owner.")
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = userAccount
            restaurant.restaurantName = form.cleaned_data["restaurantName"]
            restaurant.category = form.cleaned_data["category"]
            restaurant.address = form.cleaned_data["address"]
            if 'logo' in request.FILES:
                logo_extension = request.FILES['logo']._name.split(".")[-1]
                request.FILES['logo']._name = ".".join([slugify(restaurant.restaurantName), logo_extension])
                restaurant.logo = request.FILES['logo']
            restaurant.save()
            return redirect(reverse('other:addRestaurantDone'))
        else:
            return render(request, "other/add_restaurant.html", context={"form":form, "errors":form.errors})
    else:
        form = RestaurantForm()
        return render(request, "other/add_restaurant.html", context={"form":form, "errors":None})


@login_required
def addRestaurantDone(request):
    return render(request, 'other/add_restaurant_done.html')


@login_required
def viewRestaurantReviews(request, restaurantNameSlugged):
    # TODO
    return redirect(reverse('other:index'), kwargs={})


@login_required
def reviewRestaurant(request, restaurantNameSlugged):
    try:
        user_account = UserAccount.objects.get(user=request.user)
        restaurant = Restaurant.objects.get(restaurantNameSlugged=restaurantNameSlugged)
        if restaurant.owner == user_account:
            return redirect(reverse('other:viewRestaurantReviews', kwargs={
                'restaurantNameSlugged':restaurantNameSlugged
            }))
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                rating = form.cleaned_data['rating']
                if rating < 1 or rating > 10:
                    form.errors['rating'] = ["Rating must be between 1 and 10"]
                    return render(request, 'other/review_restaurant.html', context={
                        'form': form, 'errors': form.errors, 'restaurant': restaurant
                    })
                Review.objects.create(reviewer=user_account, restaurant=restaurant,
                rating=form.cleaned_data['rating'], comment=form.cleaned_data['comment'])
                return redirect(reverse('other:viewRestaurantReviews', kwargs={
                    'restaurantNameSlugged':restaurantNameSlugged
                }))
            else:
                return render(request, 'other/review_restaurant.html', context={
                    'form': form, 'errors': form.errors, 'restaurant': restaurant
                })
        else:
            form = ReviewForm()
            return render(request, 'other/review_restaurant.html', context={
                    'form': form, 'errors': None, 'restaurant': restaurant
                })
    except Restaurant.DoesNotExist:
        return redirect(reverse('other:index'), kwargs={})
