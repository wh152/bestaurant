from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from accounts.models import *
from accounts.forms import AdvertiseForm, RestaurantForm
from search.forms import *


@login_required
def viewOwnRestaurants(request):

    user = User.objects.get(username=request.user.username)
    userAccount = UserAccount.objects.get(user=user)
    if not userAccount.restaurantOwner:
        return redirect(reverse('other:viewOneUser', kwargs={
            "username_slug": userAccount.username_slug
        }))
    restaurants = Restaurant.objects.filter(owner=userAccount)
    # the restaurants owned that have not yet been advertised - 
    # these will be needed to decide whether to show the advertise button
    notAdvertised = list(set(restaurants) - set(removeNotAdvertised(restaurants)))
    context = {"restaurants": restaurants, "notAdvertised": notAdvertised}
    return render(request, 'other/all_owned_restaurants.html', context=context)


def viewAllUsers(request):

    return render(request, 'other/all_users.html', context={"users": UserAccount.objects.all()})


def viewOneUser(request, username_slug):

    try:
        user_account = UserAccount.objects.get(username_slug=username_slug)
        context = {}
        context["username"] = user_account.user.username
        context["username_slug"] = user_account.username_slug
        context["restaurantOwner"] = user_account.restaurantOwner
        context["about"] = user_account.about if len(user_account.about) > 0 else None
        context["photo"] = user_account.photo
        if context["photo"]:
            # get the profile photo path so it can be displayed
            context["photo_path"] = context["photo"].__str__() 
        else:
            context["photo_path"] = "profile_images/default.jpg"
        if request.user == user_account.user:
            context["own_account"] = True
        else:
            context["own_accounts"] = False
        if user_account.restaurantOwner:
            # only want other users to view restaurants you are advertising
            owned = removeNotAdvertised(Restaurant.objects.filter(owner=user_account))
            restaurants = [(r, r.restaurantNameSlugged) for r in owned]
            context["restaurants"] = restaurants if len(restaurants) > 0 else None
        else:
            context["restaurants"] = None
        print("context", context)
        return render(request, 'other/one_user.html', context=context)
    except User.DoesNotExist:
        return render(reverse('other:index'))


@login_required
def becomeRestaurantOwner(request, username_slug):
    
    if request.user.is_authenticated:
        try:
            userAccount = UserAccount.objects.get(username_slug=username_slug)
            userAccount.restaurantOwner = True
            userAccount.save()
        except UserAccount.DoesNotExist:
            pass
    return redirect(reverse('other:viewOneUser', kwargs={
        "username_slug": userAccount.username_slug
    }))


@login_required
def advertise(request):

    userAccount = UserAccount.objects.get(user=request.user)
    if not userAccount.restaurantOwner:
        return redirect(reverse('other:viewOneUser', kwargs={
            "username_slug": userAccount.username_slug
        }))
    restaurantsOwned = Restaurant.objects.filter(owner=userAccount)
    notAdvertised = []
    for restaurant in restaurantsOwned:
        if not Advertisement.objects.filter(restaurant=restaurant):
            notAdvertised.append((restaurant.restaurantID, restaurant.restaurantName))
    # can't advertise if you have no restaurants that haven't already got an advert
    if len(notAdvertised) == 0:
        return redirect(reverse('other:viewOneUser', kwargs={
            "username_slug": userAccount.username_slug
        }))
    if request.method == "POST":
        form = AdvertiseForm(userAccount, request.POST, request.FILES)
        if form.is_valid():
            restaurant = Restaurant.objects.get(restaurantID=int(form.cleaned_data['restaurant']))
            description = form.cleaned_data['description']
            advertImage = request.FILES['advertImage']
            # gets the file extensions (for compatability) by getting the letters after the last dot
            image_extension = request.FILES['advertImage']._name.split(".")[-1]
            # create the advertisement image path
            request.FILES['advertImage']._name = ".".join([restaurant.restaurantNameSlugged, image_extension])
            Advertisement.objects.create(restaurant=restaurant, description=description, 
                                        advertImage=advertImage)
            return redirect(reverse('other:viewOneUser', kwargs={
                "username_slug": userAccount.username_slug
            }))
        else:
            return render(request, "other/create_advertisement.html", {"form": form})
    else:
        form = AdvertiseForm(userAccount)
        return render(request, "other/create_advertisement.html", {"form": form})

@login_required
def addRestaurant(request):

    userAccount = UserAccount.objects.get(user=request.user)
    if not userAccount.restaurantOwner:
        return render(reverse('other:index'))
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
            return redirect(reverse('other:viewOwnRestaurants'))
        else:
            return render(request, "other/add_restaurant.html", context={"form":form, "errors":form.errors})
    else:
        form = RestaurantForm()
        return render(request, "other/add_restaurant.html", context={"form":form, "errors":None})


@login_required
def deleteRestaurant(request, restaurantNameSlugged):

    userAccount = UserAccount.objects.get(user=request.user)
    if not userAccount.restaurantOwner:
        return render(reverse('other:index'))
    restaurant = Restaurant.objects.get(restaurantNameSlugged=restaurantNameSlugged)
    # only owners of restaurants should be able to delete their own restaurants
    if not (restaurant.owner == userAccount):
        return redirect(reverse('other:viewOneUser'), kwargs={
            "username_slug": userAccount.username_slug
        })
    else:
        restaurant.delete()
    return redirect(reverse('other:viewOwnRestaurants'))


@login_required
def viewRestaurantReviews(request, restaurantNameSlugged):

    try:
        restaurant = Restaurant.objects.get(restaurantNameSlugged=restaurantNameSlugged)
        context = {}
        context['restaurants'] = [restaurant]
        if restaurant.averageRating:
            context['averageRating'] = round(restaurant.averageRating, 2)
        else:
            context['averageRating'] = None
        context['photo_path'] = restaurant.logo.__str__()
        context['reviews'] = []
        # get the reviews for the restaurant and their data
        for review in Review.objects.filter(restaurant=restaurant):
            context['reviews'].append({
                'profile_photo_path': review.reviewer.photo.__str__(),
                'reviewer': review.reviewer,
                'rating': review.rating,
                'comment': review.comment,
                'date': review.date,
            })
        return render(request, 'other/view_restaurant.html', context=context)
    except Restaurant.DoesNotExist:
        print("Failed to find", restaurantNameSlugged)
        return redirect(reverse('other:index'), kwargs={})


@login_required
def reviewRestaurant(request, restaurantNameSlugged):

    try:
        user_account = UserAccount.objects.get(user=request.user)
        restaurant = Restaurant.objects.get(restaurantNameSlugged=restaurantNameSlugged)
        # restaurant owners can't review their own restaurants
        if restaurant.owner == user_account:
            return redirect(reverse('other:viewRestaurantReviews', kwargs={
                'restaurantNameSlugged':restaurantNameSlugged
            }))
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                rating = form.cleaned_data['rating']
                # verify that the rating is between 1 and 10
                if rating < 1 or rating > 10:
                    form.errors['rating'] = ["Rating must be between 1 and 10"]
                    return render(request, 'other/review_restaurant.html', context={
                        'form': form, 'errors': form.errors, 'restaurant': restaurant
                    })
                Review.objects.create(reviewer=user_account, restaurant=restaurant,
                rating=form.cleaned_data['rating'], comment=form.cleaned_data['comment'])
                restaurant.averageRating = restaurant.average_rating()
                restaurant.save()
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

    
# helper func to remove restaurants without an advertisement
def removeNotAdvertised(restaurants):

    containsAdvertisement = []
    for restaurant in restaurants:
        try:
            Advertisement.objects.get(restaurant=restaurant)
            containsAdvertisement.append(restaurant)
        except Advertisement.DoesNotExist:
            pass
    return containsAdvertisement
