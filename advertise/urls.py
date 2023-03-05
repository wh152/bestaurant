from django.urls import path
from . import views

app_name = 'advertise'

urlpatterns = [
    path('', views.createAdvert, name='createAdvert'),
]