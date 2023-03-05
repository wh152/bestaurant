from accounts.models import *
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

def viewAllUsers(request):
    return render(request, 'user/all_users.html', context={"allUsers": UserAccount.objects.all()})

def viewOneUser(request, username):
    try:
        user = User.objects.get(username=username)
        userAccount = UserAccount.objects.get(user=user)
        context = {}
        context["username"] = user.username
        context["restaurantOwner"] = userAccount.restaurantOwner
        context["about"] = userAccount.about if len(userAccount.about) > 0 else None
        context["photo"] = userAccount.photo
        context["recentlyReviewed"] = userAccount.recentlyReviewed
        if userAccount.restaurantOwner:
            restaurants = [restaurant for restaurant in Restaurant.objects.filter(owner=userAccount)]
            context["restaurants"] = restaurants if len(restaurants) > 0 else None
        else:
            context["restaurants"] = None
        return render(request, 'user/one_user.html', context=context)
    except User.DoesNotExist:
        return HttpResponse("Requested user does not exist")