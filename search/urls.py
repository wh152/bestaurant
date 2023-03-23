from django.urls import path

from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_results, name='search_results'),
    # the 3 filters for all advertisements
    path('most-reviewed/', views.most_reviewed, name='most_reviewed'),
    path('most-recently-reviewed/', views.most_recently_reviewed, name='most_recently_reviewed'),
    path('recently-added/', views.recently_added, name='recently_added'),
    # filtering by category
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
]