from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.template.defaultfilters import slugify
from django.test import Client, TestCase
from django.urls import path, reverse

from accounts.forms import (AdvertiseForm, LoginForm, RegistrationForm,
                            RestaurantForm)
from accounts.models import Advertisement, Restaurant, UserAccount
from other import views as other_views
from search.models import Review


# model tests
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


# view tests
class ViewTests(TestCase):
    def test_register_view(self):
        # tests if the appropriate header buttons are present for non-logged in
        client = Client()
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'Register for Bestaurant!')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Log In')
        self.assertContains(response, 'Google')
        self.assertNotContains(response, 'My Account')
        self.assertNotContains(response, 'Sign Out')

    def test_user_login_view(self):
        client = Client()
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'Please enter your username and password')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Log In')
        self.assertContains(response, 'Google')
        self.assertNotContains(response, 'My Account')
        self.assertNotContains(response, 'Sign Out')

    def my_account_view(self):
        # test if a user's personal account page has their username and accounts description
        client = Client()
        test_user = User.objects.create(email="test@mail.com",username="usertest", password="testpass")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        test_account.save()
        path('user/<str:username_slug>', other_views.viewOneUser, name='viewOneUser'),
        response = self.client.get(reverse('viewOneUser', args =[test_account.username_slug]))
        self.assertContains(response, test_account.user.username)
        self.assertContains(response, test_account.about)

    
# forms tests used with both valid and invalid data
class AccountsForms(TestCase):
    def test_registration_form(self):

        form_data = {
            'email': 'test@mailtest.com',
            'username': 'test',
            'password': 'password',
            'confirm_password': 'password',

        }

        empty_data = {}
        
        form_one = RegistrationForm(data=form_data)
        form_two = RegistrationForm(data=empty_data)
        self.assertTrue(form_one.is_valid())
        self.assertFalse(form_two.is_valid())


    def test_restaurant_form(self):
        restaurant_data = {
            'restaurantName': 'test= restaurant',
            'category': 'Casual Dining',
            'address': '12 Hillview Drive',
        }

        invalid_category_data = {
            'restaurantName': 'test= restaurant',
            'category': 'Chip Shop',
            'address': '12 Hillview Drive',
        }

        empty_data = {}

        form_one = RestaurantForm(data=restaurant_data)
        form_two = RestaurantForm(data=invalid_category_data)
        form_three = RestaurantForm(data=empty_data)

        self.assertTrue(form_one.is_valid())
        self.assertFalse(form_two.is_valid())
        self.assertFalse(form_three.is_valid())


    def test_login_form(self):
        login_data_username = {
            'username_or_email': 'test_username',
            'password': 'test',
        }

        login_data_email = {
            'username_or_email': 'test@testmail.com',
            'password': '1234567',
        }

        login_data_no_password = {
            'username_or_email' :'username_test',
        }

        empty_data = {}

        form_one = LoginForm(data=login_data_username)
        form_two = LoginForm(data=login_data_email)
        form_three = LoginForm(data=login_data_no_password)
        form_four = LoginForm(data=empty_data)

        self.assertTrue(form_one.is_valid())
        self.assertTrue(form_two.is_valid())
        self.assertFalse(form_three.is_valid())
        self.assertFalse(form_four.is_valid())


    def test_advertisement_form(self):
        # tests that all fields are required to make an advertisement
        test_user = User.objects.create(email="test@mail.com",username="usertest", password="testpass")
        test_account = UserAccount.objects.create(user=test_user, username_slug = models.SlugField )
        test_restaurant = Restaurant.objects.create(restaurantID = 1, restaurantName="The Bestaurant", owner=test_account)
        test_restaurant.save()

        
        advert_file = open('static/images/logo.jpeg', 'rb')

        advertisement_data = {
            'restaurant' : test_restaurant.restaurantID,
            'description': 'best restaurant ever',
        }

        files = {
            'advertImage': SimpleUploadedFile(advert_file.name, advert_file.read())
        }

        advertisement_no_restaurant_data = {
            'description': 'worst restaurant ever',
        }

        empty_data = {}

        form_one = AdvertiseForm(user=test_account, data=advertisement_data, files = files)
        form_two = AdvertiseForm(user=test_account, data=advertisement_no_restaurant_data)
        form_three = AdvertiseForm(user=test_account, data=empty_data)

        self.assertTrue(form_one.is_valid())
        self.assertFalse(form_two.is_valid())
        self.assertFalse(form_three.is_valid())
