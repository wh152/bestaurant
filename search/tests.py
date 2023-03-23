from django.test import TestCase, Client
from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserAccount, Restaurant, Advertisement
from search.models import Review, Category
from django.template.defaultfilters import slugify
from django.urls import path, reverse
from datetime import datetime
from search.forms import ReviewForm

# Create your tests here.

#model tests
class TestReviewModel(TestCase):
    def test_review_instance(self):
        test_user = User.objects.create(email="test@mail.com",username="usertest", password="testpass")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        test_restaurant = Restaurant.objects.create(restaurantID = 1, restaurantName="The Bestaurant", owner=test_account)
        test_review = Review.objects.create(reviewID =1, reviewer=test_account, restaurant=test_restaurant, rating=5, comment="food was good")
        self.assertIsInstance(test_review, Review)

    def test_review_str(self):
        test_user = User.objects.create(email="test@mail.com",username="usertest", password="testpass")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        test_restaurant = Restaurant.objects.create(restaurantID = 1, restaurantName="The Bestaurant", owner=test_account)
        test_review = Review.objects.create(reviewID =1, reviewer=test_account, restaurant=test_restaurant, rating=5, comment="lovely food")
        test_review.save()
        self.assertEqual(str(test_review), '1 - The Bestaurant - usertest - 5 - lovely food')
        self.assertNotEqual(str(test_review), '1 - My restaurant - usertest - 5 - lovely food')


class TestCategoryModel(TestCase):
    def test_category_instance(self):
        test_category = Category.objects.create(name="test_category")
        self.assertIsInstance(test_category, Category)

    def test_category_str(self):
        test_category = Category.objects.create(name="test_category")
        test_category.save()
        self.assertEqual(str(test_category), 'test_category')


    def test_category_save(self):
        test_category = Category.objects.create(name="test_category")
        test_category.save()
        self.assertEqual(test_category.slug, slugify(test_category.name))

#views tests

class SearchViewTests(TestCase):
    def test_index_view(self):
        client = Client()

        test_user_one = User.objects.create(email="test@mail.com",username="usertest", password="testpass")
        test_account_one = UserAccount.objects.create(user=test_user_one, username_slug = models.SlugField )

        test_user_two = User.objects.create(email="second_test@mail.com",username="usertwo", password="test")
        test_account_two = UserAccount.objects.create(user=test_user_two, username_slug = models.SlugField )

        test_restaurant_one = Restaurant.objects.create(restaurantID = 1, restaurantName="The Bestaurant", owner=test_account_one, address="72 hillview lane", averageRating = 10)
        test_restaurant_one.save()
        test_restaurant_two = Restaurant.objects.create(restaurantID = 2, restaurantName="The Oak Cafe", owner=test_account_one, address="17 newton crescent", averageRating=5)
        test_restaurant_two.save()
        test_restaurant_three = Restaurant.objects.create(restaurantID = 3, restaurantName="Treehouse", owner=test_account_two, address="46 main street", averageRating = 2)
        test_restaurant_three.save()
        test_restaurant_four = Restaurant.objects.create(restaurantID = 4, restaurantName="Cafe 14", owner=test_account_two, address="95 high street", averageRating =7)
        test_restaurant_four.save()

        response = self.client.get(reverse('other:index'))

        self.assertContains(response, test_restaurant_one.restaurantName)
        self.assertContains(response, test_restaurant_two.restaurantName)
        self.assertContains(response, test_restaurant_four.restaurantName)
        self.assertNotContains(response, test_restaurant_three.restaurantName)

    def test_search_results_view(self):
        client = Client()
        test_user = User.objects.create(email="test@mail.com",username="user", password="test")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        
        test_restaurant = Restaurant.objects.create(restaurantID = 1, restaurantName="Cafe 14", owner=test_account, address="95 high street")
        test_advert = Advertisement.objects.create(restaurant= test_restaurant, description="We have food")
        test_advert.save()

        response = self.client.get(reverse('search:search_results') + "?q=" + test_restaurant.restaurantName)
        self.assertEqual(response.context['restaurants'], [test_restaurant])

    def test_show_category_view(self):
        client = Client()
        test_category = Category.objects.create(name="Fast Food")
        test_category.save()

        test_user = User.objects.create(email="test@mail.com",username="user", password="test")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        
        test_restaurant_one = Restaurant.objects.create(restaurantID = 1, restaurantName="Greggs", owner=test_account, address="95 high street", category="Fast Food")
        test_advert_one = Advertisement.objects.create(restaurant= test_restaurant_one, description="We have food")
        test_advert_one.save()

        test_restaurant_two = Restaurant.objects.create(restaurantID = 2, restaurantName="KFC", owner=test_account, address="53 union street", category="Fast Food")
        test_advert_two = Advertisement.objects.create(restaurant= test_restaurant_two, description="We have more food")
        test_advert_two.save()

        test_restaurant_three = Restaurant.objects.create(restaurantID = 3, restaurantName="The Oak Cafe", owner=test_account, address="45 gatwick street", category="Casual Dining")
        test_advert_three = Advertisement.objects.create(restaurant= test_restaurant_three, description="Casual dining cafe")
        test_advert_three.save()

        response = self.client.get(reverse('search:show_category', args =[test_category.slug]) + "?q=" + test_category.slug)

        self.assertEqual(response.context['restaurants'], [test_restaurant_one, test_restaurant_two])
        

    def test_most_reviewed(self):
        client = Client()

        reviewer_one = User.objects.create(email="r@mail.com",username="reviewone", password="reviewpass")
        reviewer_one_account = UserAccount.objects.create(user=reviewer_one, username_slug = models.SlugField )

        reviewer_two = User.objects.create(email="rt@mail.com",username="reviewtwo", password="password")
        reviewer_two_account = UserAccount.objects.create(user=reviewer_two, username_slug = models.SlugField )
        
        owner = User.objects.create(email="ro@mail.com",username="boss", password="bosspass")
        owner_account = UserAccount.objects.create(user=owner, username_slug = models.SlugField )

        test_restaurant_one = Restaurant.objects.create(restaurantID = 1, restaurantName="The Bestaurant", owner=owner_account, address="72 hillview lane")
        test_restaurant_one.save()
        test_restaurant_two = Restaurant.objects.create(restaurantID = 2, restaurantName="The Oak Cafe", owner=owner_account, address="17 newton crescent")
        test_restaurant_two.save()
        test_restaurant_three = Restaurant.objects.create(restaurantID = 3, restaurantName="Treehouse", owner=owner_account, address="46 main street")
        test_restaurant_three.save()
        test_restaurant_four = Restaurant.objects.create(restaurantID = 4, restaurantName="Greggs", owner=owner_account, address="289 tennant road")
        test_restaurant_four.save()

        review_one = Review.objects.create(reviewID =1, reviewer=reviewer_one_account, restaurant=test_restaurant_one, rating=10, comment="lovely food")
        review_one.save()
        review_two = Review.objects.create(reviewID =2, reviewer=reviewer_two_account, restaurant=test_restaurant_one, rating=5, comment="nice enough")
        review_two.save()
        review_three = Review.objects.create(reviewID =3, reviewer=reviewer_one_account, restaurant=test_restaurant_two, rating=6, comment="good staff")
        review_three.save()
        review_four = Review.objects.create(reviewID =4, reviewer=reviewer_one_account, restaurant=test_restaurant_three, rating=10, comment="wonderful")
        review_four.save()
        review_five = Review.objects.create(reviewID =5, reviewer=reviewer_two_account, restaurant=test_restaurant_three, rating=3, comment="wasn't for me")
        review_five.save()
        
        response = self.client.get(reverse('search:most_reviewed'))

        self.assertContains(response, test_restaurant_one.restaurantName)
        self.assertContains(response, test_restaurant_two.restaurantName)
        self.assertContains(response, test_restaurant_three.restaurantName)
        self.assertNotContains(response, test_restaurant_four.restaurantName)

    def test_recently_reviewed_view(self):
        reviewer = User.objects.create(email="r@mail.com",username="review", password="reviewpass")
        reviewer_account = UserAccount.objects.create(user=reviewer, username_slug = models.SlugField )
        
        owner = User.objects.create(email="ro@mail.com",username="boss", password="bosspass")
        owner_account = UserAccount.objects.create(user=owner, username_slug = models.SlugField )

        test_restaurant_one = Restaurant.objects.create(restaurantID = 1, restaurantName="The Bestaurant", owner=owner_account, address="72 hillview lane")
        test_restaurant_one.save()
        test_restaurant_two = Restaurant.objects.create(restaurantID = 2, restaurantName="The Oak Cafe", owner=owner_account, address="17 newton crescent")
        test_restaurant_two.save()
        test_restaurant_three = Restaurant.objects.create(restaurantID = 3, restaurantName="Treehouse", owner=owner_account, address="46 main street")
        test_restaurant_three.save()
        test_restaurant_four = Restaurant.objects.create(restaurantID = 4, restaurantName="Greggs", owner=owner_account, address="289 tennant road")
        test_restaurant_four.save()

        review_one = Review.objects.create(reviewID =1, reviewer=reviewer_account, restaurant=test_restaurant_one, rating=10, comment="lovely food")
        review_one.date = datetime(2018, 9, 15)
        review_one.save()

        review_two = Review.objects.create(reviewID =2, reviewer=reviewer_account, restaurant=test_restaurant_two, rating=5, comment="nice enough")
        review_two.date = datetime(2017, 5, 7)
        review_two.save()

        review_three = Review.objects.create(reviewID =3, reviewer=reviewer_account, restaurant=test_restaurant_three, rating=6, comment="good staff")
        review_three.date = datetime(2012, 10, 30)
        review_three.save()

        review_four = Review.objects.create(reviewID =4, reviewer=reviewer_account, restaurant=test_restaurant_four, rating=10, comment="wonderful")
        review_four.date = datetime(2019, 2, 3)
        review_four.save()

        response = self.client.get(reverse('search:most_recently_reviewed'))

        self.assertContains(response, test_restaurant_one.restaurantName)
        self.assertContains(response, test_restaurant_two.restaurantName)
        self.assertContains(response, test_restaurant_four.restaurantName)
        self.assertNotContains(response, test_restaurant_three.restaurantName)

    def test_recently_added(self):
        owner = User.objects.create(email="ro@mail.com",username="boss", password="bosspass")
        owner_account = UserAccount.objects.create(user=owner, username_slug = models.SlugField )

        test_restaurant_one = Restaurant.objects.create(restaurantID = 1, restaurantName="The Bestaurant", owner=owner_account, address="72 hillview lane")
        test_restaurant_one.dateAdded = datetime(2008, 6, 1)
        test_restaurant_one.save()

        test_restaurant_two = Restaurant.objects.create(restaurantID = 2, restaurantName="The Oak Cafe", owner=owner_account, address="17 newton crescent")
        test_restaurant_two.dateAdded = datetime(2011, 5, 29) 
        test_restaurant_two.save()

        test_restaurant_three = Restaurant.objects.create(restaurantID = 3, restaurantName="Treehouse", owner=owner_account, address="46 main street")
        test_restaurant_two.dateAdded = datetime(2017, 10, 8) 
        test_restaurant_three.save()

        test_restaurant_four = Restaurant.objects.create(restaurantID = 4, restaurantName="Greggs", owner=owner_account, address="289 tennant road")
        test_restaurant_two.dateAdded = datetime(2015, 12, 9) 
        test_restaurant_four.save()

        response = self.client.get(reverse('search:recently_added'))

        self.assertContains(response, test_restaurant_two.restaurantName)
        self.assertContains(response, test_restaurant_three.restaurantName)
        self.assertContains(response, test_restaurant_four.restaurantName)
        self.assertNotContains(response, test_restaurant_one.restaurantName)


#forms tests
class SearchFormTest(TestCase):

    def test_review_form(self):
        form_data = {
            'rating': 9,
            'comment': 'great place',
        }

        form_data_no_comment = {
            'rating' : 5,
        }

        form_data_invalid_rating_high ={
            'rating' : 168,
            'comment' : 'top quality'
        }

        form_data_invalid_rating_low ={
            'rating' : -8,
            'comment' : 'bad'
        }

        empty_data = {}

        
        form_one = ReviewForm(data=form_data)
        form_two = ReviewForm(data=form_data_no_comment)
        form_three = ReviewForm(data=form_data_invalid_rating_high)
        form_four = ReviewForm(data=form_data_invalid_rating_low)
        form_five = ReviewForm(data=empty_data)

        self.assertTrue(form_one.is_valid())
        self.assertFalse(form_two.is_valid())
        self.assertFalse(form_three.is_valid())
        self.assertFalse(form_four.is_valid())
        self.assertFalse(form_five.is_valid())


    