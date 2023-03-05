from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.viewAllUsers, name='viewAllUsers'),
    path('<str:username>/', views.viewOneUser, name='viewOneUser'),
]