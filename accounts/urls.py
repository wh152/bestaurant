from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('rate/<int:rating>/', views.rate),
]