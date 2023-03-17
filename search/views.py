from django.shortcuts import render
from accounts.models import *
from django.db.models import Q, Count
from search.models import Category, Review
from accounts.models import *


def index(request):
    restaurant_list = Restaurant.objects.order_by('-averageRating')[:3]

    context_dict = {}
    context_dict['restaurants'] = restaurant_list

    response = render(request, 'search/index.html', context=context_dict)
    
    return response


def search_results(search_request):

    model = Restaurant
    restaurant_list = []

    if search_request.method == 'GET':
        query = search_request.Get.get('q')
        if query:
            restaurant_list = model.filter(
                Q(owner__icontains=query) | Q(restaurantName__icontains=query) | Q(address__icontains=query)
            )

    return render(search_request, 'search/search_results.html', {'restaurant_list': restaurant_list})


def show_category(request, category_name_slug):

    context_dict = {}

    category = Category.objects.get(slug=category_name_slug)
    restaurants = Restaurant.objects.filter(category=category)
    context_dict['category'] = category
    context_dict['restaurants'] = restaurants

    return render(request, 'search/category.html', context=context_dict)


def most_reviewed(request):
    
    restaurant_list = Restaurant.objects.all().annotate(num_reviews=Count('review')).order_by('-num_reviews')

    context_dict = {}
    context_dict['restaurants'] = restaurant_list

    return render(request, 'search/most_reviewed.html', context=context_dict)
    
    
    
def most_recently_reviewed(request):
    
    review_list = Review.objects.order_by('-date')
    restaurant_list = Restaurant.objects.all()
    
    restaurant_list.union(review_list, all-True)

    context_dict = {}
    context_dict['restaurants'] = restaurant_list

    return render(request, 'search/sort_most_recently_reviewed.html', context=context_dict)
    
    
    
def recently_added(request):
    
    restaurant_list = Restaurant.objects.order_by('-dateAdded')

    context_dict = {}
    context_dict['restaurants'] = restaurant_list

    return render(request, 'search/sort_recently_added.html', context=context_dict)

