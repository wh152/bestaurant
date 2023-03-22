from django.db.models import Count, Q
from django.shortcuts import render

from accounts.models import *
from other.views import removeNotAdvertised
from search.models import Category, Review


def index(request):

    context_dict = {}
    if request.user.is_authenticated:
        try:
            # if a user has used Google then they will have a 
            # User object but not a UserAccount, this creates
            # one for them which they can edit later
            UserAccount.objects.get(user=request.user)
            context_dict["google"] = False
            context_dict["username"] = request.user.username
            context_dict['userAccount'] = UserAccount.objects.get(user=request.user)
        except UserAccount.DoesNotExist:
            userAccount = UserAccount.objects.create(user=request.user, restaurantOwner=False)
            context_dict["google"] = True
            context_dict["username"] = request.user.username
            context_dict['userAccount'] = userAccount
    else:
        context_dict["google"] = False
        context_dict["username"] = None
        context_dict['userAccount'] = None
    # selects the 3 highest rated restaurants
    restaurant_list = Restaurant.objects.order_by('-averageRating')[:3]

    context_dict['restaurants'] = restaurant_list
    response = render(request, 'search/index.html', context=context_dict)
    
    return response


def search_results(search_request):

    context = {}
    restaurant_list = []

    if search_request.method == 'GET':
        query = search_request.GET.get('q')
        context['query'] = query
        if query:
            # selects advertisements with the query in its
            # description, name, address or owner's name
            advertisement_list = Advertisement.objects.filter(
                Q(description__icontains=query) | Q(restaurant__restaurantName__icontains=query) | 
                Q(restaurant__address=query) | Q(restaurant__owner__user__username__icontains=query)
            )
            restaurant_list = []
            for advert in advertisement_list:
                restaurant = Restaurant.objects.get(restaurantID=advert.restaurant.restaurantID)
                restaurant_list.append(restaurant)
    context['restaurants'] = restaurant_list
    context['searching'] = True
    context['query'] = query

    return render(search_request, 'search/search_results.html', context=context)


def show_category(request, category_name_slug):

    context_dict = {}
    category = Category.objects.get(slug=category_name_slug)
    context_dict['restaurants'] = removeNotAdvertised(Restaurant.objects.filter(category=category))
    return render(request, 'search/search_results.html', context=context_dict)


def most_reviewed(request):
    
    # orders restaurants by the count of their reviews
    # in descending order and selects the top 3
    restaurant_list = Restaurant.objects.all().annotate(num_reviews=Count('review')).order_by('-num_reviews')[:3]

    context_dict = {}
    context_dict['restaurants'] = restaurant_list
    context_dict['searching'] = False
    context_dict['query'] = "Most Reviewed"

    return render(request, 'search/search_results.html', context=context_dict)
    
    
    
def most_recently_reviewed(request):
    
    # sorts all reviews by date descending (latest first)
    review_list = Review.objects.order_by('-date')
    restaurant_list = []
    for review in review_list:
        restaurant = Restaurant.objects.get(restaurantID=review.restaurant.restaurantID)
        if restaurant not in restaurant_list:
            restaurant_list.append(restaurant)
            # when 3 restaurants have been added stop going over the sorted reviews
            if len(restaurant_list) == 3:
                break

    context_dict = {}
    context_dict['restaurants'] = restaurant_list
    context_dict['searching'] = False
    context_dict['query'] = "Most Recently Reviewed"

    return render(request, 'search/search_results.html', context=context_dict)
    
    
    
def recently_added(request):
    
    # order restaurants by their date added in 
    # descending order and select the top 3
    restaurant_list = Restaurant.objects.order_by('-dateAdded')[:3]

    context_dict = {}
    context_dict['restaurants'] = restaurant_list
    context_dict['searching'] = False
    context_dict['query'] = "Recently Added"

    return render(request, 'search/search_results.html', context=context_dict)

