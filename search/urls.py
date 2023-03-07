from django.urls import path

from .views import search_results, show_category

urlpatterns = [path("search/", search_results, name = 'search_results'),
               #urls for sorting buttons on home page
               path('category/<slug:category_name_slug>/', show_category, name='show_category'),
               ]