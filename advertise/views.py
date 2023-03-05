from accounts.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import AdvertisementForm

@login_required
def createAdvert(request, restaurantID):
    form = AdvertisementForm()
    context = {"form": form, "restaurantID": restaurantID, "errors": None}
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, '')
        else:
            context["errors"] = form.errors
    return render(request, 'create_advertisement.html', context=context)
