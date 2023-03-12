from django.urls import path
from . import views

app_name = 'other'

urlpatterns = [
    # path('advertise/', views.createAdvert, name='createAdvert'),
    path('managerestaurants/', views.viewOwnRestaurants, name='viewOwnRestaurants'),
    path('managerestaurants/add/', views.addRestaurant, name='addRestaurant'),
    path('managerestaurants/add/done/', views.addRestaurantDone, name='addRestaurantDone'),
    path('user/', views.viewAllUsers, name='viewAllUsers'),
    path('user/<str:username_slug>', views.viewOneUser, name='viewOneUser'),
    path('advertise/', views.advertise, name='advertise'),
    path('advertise/success/', views.advertiseSuccess, name='advertiseSuccess'),
    path('', views.index, name='index'),
]