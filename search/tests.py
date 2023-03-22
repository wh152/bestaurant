from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserAccount, Restaurant, Advertisement
from search.models import Review, Category
from django.template.defaultfilters import slugify

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


