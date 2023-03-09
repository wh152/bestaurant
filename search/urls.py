from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path("", views.search_results, name='search_results'),
    #urls for sorting buttons on home page
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
]