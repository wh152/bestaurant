from django.urls import path
from . import views

app_name = 'managerestaurants'

urlpatterns = [
    path('', views.viewOwnRestaurants, name='viewOwnRestaurants'),
    # path('<str:restaurantName>/', views.viewOwnRestaurants, name='viewOwnRestaurants'),
]