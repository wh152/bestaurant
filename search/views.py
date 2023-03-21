from django.shortcuts import render
from accounts.models import *
from django.db.models import Q, Count
from search.models import Category, Review
from accounts.models import *


def index(request):
    print("INSIDE INDEX")
    restaurant_list = Restaurant.objects.order_by('-averageRating')[:3]

    context_dict = {}
    context_dict['restaurants'] = restaurant_list

    response = render(request, 'search/index.html', context=context_dict)
    
    return response


def search_results(search_request):

    print("INSIDE SEARCH_RESULTS")

    context = {}
    restaurant_list = []

    if search_request.method == 'GET':
        query = search_request.GET.get('q')
        context['query'] = query
        if query:
            advertisement_list = Advertisement.objects.filter(
                Q(description__icontains=query) | Q(restaurant__restaurantName__icontains=query) | 
                Q(restaurant__address=query) | Q(restaurant__owner__user__username__icontains=query)
            )
            restaurant_list = [Restaurant.objects.get(restaurantID=advert.restaurant.restaurantID) for advert in advertisement_list]
    context['restaurant_list'] = restaurant_list

    return render(search_request, 'search/search_results.html', context=context)


def show_category(request, category_name_slug):

    print("INSIDE SHOW_CATEGORY")

    context_dict = {}

    category = Category.objects.get(slug=category_name_slug)
    restaurants = Restaurant.objects.filter(category=category)
    context_dict['category'] = category
    context_dict['restaurants'] = restaurants

    return render(request, 'search/category.html', context=context_dict)


def most_reviewed(request):

    print("INSIDE MOST_REVIEWED")
    
    restaurant_list = Restaurant.objects.all().annotate(num_reviews=Count('review')).order_by('-num_reviews')[:3]

    context_dict = {}
    context_dict['restaurants'] = restaurant_list

    return render(request, 'search/most_reviewed.html', context=context_dict)
    
    
    
def most_recently_reviewed(request):

    print("INSIDE MOST_RECENTLY_REVIEWED")
    
    review_list = Review.objects.order_by('-date')[:3]
    restaurant_list = []
    for review in review_list:
        restaurant = Restaurant.objects.get(restaurantID=review.restaurant.restaurantID)
        restaurant_list.append(restaurant)
    print("review_list", review_list)
    print("restaurant_list", restaurant_list)

    context_dict = {}
    context_dict['restaurants'] = restaurant_list

    return render(request, 'search/sort_most_recently_reviewed.html', context=context_dict)
    
    
    
def recently_added(request):

    print("INSIDE RECENTLY ADDED")
    
    restaurant_list = Restaurant.objects.order_by('-dateAdded')[:3]

    context_dict = {}
    context_dict['restaurants'] = restaurant_list

    return render(request, 'search/sort_recently_added.html', context=context_dict)

