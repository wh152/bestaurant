from django.test import TestCase, Client
from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserAccount, Restaurant, Advertisement
from search.models import Review
from django.template.defaultfilters import slugify
from django.test.utils import setup_test_environment

# Create your tests here.

#model tests
class TestUserAccountModel(TestCase):
    def test_user_instance(self):
        test_user = User.objects.create(email="test@mail.com",username="usertest", password="testpass")
        self.assertIsInstance(test_user, User)

    def test_user_account_instance(self):
        test_user = User.objects.create(email="test@mail.com",username="usertest", password="testpass")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        self.assertIsInstance(test_account, UserAccount)

    def test_user_account_model_save(self):
        test_user = User.objects.create(email="test@mail.com",username="User Test", password="testpass")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        test_account.save()
        self.assertEqual(test_account.username_slug, slugify(test_user.username))

    def test_user_account_model_str(self):
        test_user = User.objects.create(email="test@mail.com",username="usertest", password="testpass")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        test_account.save()
        self.assertEqual(str(test_account), 'usertest')


class TestRestaurantModel(TestCase):
    def test_restaurant_instance(self):
        test_user = User.objects.create(email="test@mail.com",username="usertest", password="testpass")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        test_restaurant = Restaurant.objects.create(restaurantID = 1, restaurantName="The Bestaurant", owner=test_account)

        self.assertIsInstance(test_restaurant, Restaurant)

    def test_restaurant_model_save(self):
        test_user = User.objects.create(email="test@mail.com",username="User Test", password="testpass")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        test_restaurant = Restaurant.objects.create(restaurantID = 1, restaurantName="The Bestaurant", owner=test_account)
        test_restaurant.save()
        self.assertEqual(test_restaurant.restaurantNameSlugged, slugify(test_restaurant.restaurantName))

    def test_restaurant_model_str(self):
        test_user = User.objects.create(email="test@mail.com",username="usertest", password="testpass")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        test_restaurant = Restaurant.objects.create(restaurantID = 1, restaurantName="The Bestaurant", owner=test_account)

        self.assertEqual(str(test_restaurant), '1: The Bestaurant')

    def test_restaurant_model_average_rating(self):
        test_owner = User.objects.create(email="test@mail.com",username="usertest", password="testpass")
        test_owner_account = UserAccount.objects.create(user=test_owner, username_slug = models.SlugField )
        test_restaurant = Restaurant.objects.create(restaurantID = 1, restaurantName="The Bestaurant", owner=test_owner_account)

        test_reviewer_one = User.objects.create(email="reviewerone@mail.com",username="reviewusertest", password="revieweronepass")
        test_reviewer_one_account = UserAccount.objects.create(user=test_reviewer_one, username_slug = models.SlugField )
        test_reviewer_two = User.objects.create(email="reviewertwo@mail.com",username="secondreviewusertest", password="reviewertwopass")
        test_reviewer_two_account = UserAccount.objects.create(user=test_reviewer_two, username_slug = models.SlugField )
        test_reviewer_three = User.objects.create(email="reviewerthree@mail.com",username="thirdreviewusertest", password="reviewerthreepass")
        test_reviewer_three_account = UserAccount.objects.create(user=test_reviewer_three, username_slug = models.SlugField )

        test_review = Review.objects.create(reviewID=1, reviewer=test_reviewer_one_account, restaurant=test_restaurant, rating=4)
        second_test_review = Review.objects.create(reviewID=2, reviewer=test_reviewer_two_account, restaurant=test_restaurant, rating=6)
        third_test_review = Review.objects.create(reviewID=3, reviewer=test_reviewer_three_account, restaurant=test_restaurant, rating=10) 

        test_review.save()
        second_test_review.save()
        third_test_review.save()

        self.assertEqual(Restaurant.average_rating(test_restaurant), 20/3)


class TestAdvertisementModel(TestCase):
    def test_advertisement_instance(self):
        test_user = User.objects.create(email="test@mail.com",username="usertest", password="testpass")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        test_restaurant = Restaurant.objects.create(restaurantID = 1, restaurantName="The Bestaurant", owner=test_account)
        test_advert = Advertisement.objects.create(restaurant= test_restaurant, description="We have food")

        self.assertIsInstance(test_advert, Advertisement)


    def test_advertisement_model_str(self):
        test_user = User.objects.create(email="test@mail.com",username="usertest", password="testpass")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        test_restaurant = Restaurant.objects.create(restaurantID = 1, restaurantName="The Bestaurant", owner=test_account)
        test_advert = Advertisement.objects.create(restaurant= test_restaurant, description="We have food")

        self.assertEquals(str(test_advert), "The Bestaurant: We have food")
