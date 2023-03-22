from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_results, name='search_results'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('', views.index, name='index'),
    path('most_reviewed',views.most_reviewed, name='most_reviewed'),
    path('most_recently_reviewed',views.most_recently_reviewed, name='most_recently_reviewed'),
    path('recently_added',views.recently_added, name='recently_added'),
]