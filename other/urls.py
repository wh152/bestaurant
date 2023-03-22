from django.urls import path
from . import views
from search import views as search_views
from accounts import views as account_views

app_name = 'other'

urlpatterns = [
    path('', search_views.index, name='index'),
    path('most_reviewed/', search_views.most_reviewed, name='most_reviewed'),
    path('most_recently_reviewed/', search_views.most_recently_reviewed, name='most_recently_reviewed'),
    path('recently_added/', search_views.recently_added, name='recently_added'),
    path('managerestaurants/', views.viewOwnRestaurants, name='viewOwnRestaurants'),
    path('managerestaurants/add/', views.addRestaurant, name='addRestaurant'),
    path('managerestaurants/add/done/', views.addRestaurantDone, name='addRestaurantDone'),
    path('managerestaurants/<str:restaurantNameSlugged>/delete/', views.deleteRestaurant, name='deleteRestaurant'),
    path('user/', views.viewAllUsers, name='viewAllUsers'),
    path('user/<str:username_slug>/', views.viewOneUser, name='viewOneUser'),
    path('user/<str:username_slug>/becomeRestaurantOwner/', views.becomeRestaurantOwner, name='becomeRestaurantOwner'),
    path('advertise/', views.advertise, name='advertise'),
    path('advertise/success/', views.advertiseSuccess, name='advertiseSuccess'),
    path('restaurant/<str:restaurantNameSlugged>/', views.viewRestaurantReviews, name='viewRestaurantReviews'),
    path('restaurant/<str:restaurantNameSlugged>/review/', views.reviewRestaurant, name='reviewRestaurant'),
    path('accounts/image/change/', account_views.change_image, name='change_image'),
    path('accounts/description/change/', account_views.change_description, name='change_description'),
]