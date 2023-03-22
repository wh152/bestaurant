from django.urls import path
from . import views
from search import views as search_views
from accounts import views as account_views

app_name = 'other'

urlpatterns = [
    # the index (home) page
    path('', search_views.index, name='index'),
    path('managerestaurants/', views.viewOwnRestaurants, name='viewOwnRestaurants'),
    path('managerestaurants/add/', views.addRestaurant, name='addRestaurant'),
    path('managerestaurants/<str:restaurantNameSlugged>/delete/', views.deleteRestaurant, name='deleteRestaurant'),
    path('user/', views.viewAllUsers, name='viewAllUsers'),
    path('user/<str:username_slug>/', views.viewOneUser, name='viewOneUser'),
    path('user/<str:username_slug>/becomeRestaurantOwner/', views.becomeRestaurantOwner, name='becomeRestaurantOwner'),
    path('advertise/', views.advertise, name='advertise'),
    path('restaurant/<str:restaurantNameSlugged>/', views.viewRestaurantReviews, name='viewRestaurantReviews'),
    path('restaurant/<str:restaurantNameSlugged>/review/', views.reviewRestaurant, name='reviewRestaurant'),
    # views to change image and description
    path('accounts/image/change/', account_views.change_image, name='change_image'),
    path('accounts/description/change/', account_views.change_description, name='change_description'),
]