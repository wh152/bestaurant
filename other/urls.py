from django.urls import path
from . import views

app_name = 'other'

urlpatterns = [
    # path('advertise/', views.createAdvert, name='createAdvert'),
    path('', views.temp, name='temp'),
    path('managerestaurants/', views.viewOwnRestaurants, name='viewOwnRestaurants'),
    path('user/', views.viewAllUsers, name='viewAllUsers'),
    path('user/<str:username>', views.viewOneUser, name='viewOneUser'),
    path('advertise/', views.advertise, name='advertise'),
]