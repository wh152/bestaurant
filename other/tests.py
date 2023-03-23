from django.test import TestCase, Client
from django.db import models
from django.urls import reverse, path
from django.contrib.auth.models import User
from accounts.models import UserAccount, Restaurant, Advertisement
from search.models import Review
from datetime import datetime

# Create your tests here.

#other views tests

class TestOtherViews(TestCase):

    def test_view_all_users(self):
        client = Client()
        user_one = User.objects.create(email="userone@mail.com",username="firstuser", password="pass")
        user_one_account = UserAccount.objects.create(user=user_one, username_slug = models.SlugField )
        user_one_account.save()

        user_two = User.objects.create(email="usertwo@mail.com",username="seconduser", password="pass")
        user_two_account = UserAccount.objects.create(user=user_two, username_slug = models.SlugField )
        user_two_account.save()

        user_three = User.objects.create(email="userthree@mail.com",username="thirduser", password="pass")
        user_three_account = UserAccount.objects.create(user=user_three, username_slug = models.SlugField )
        user_three_account.save()

        user_four = User.objects.create(email="userfour@mail.com",username="fourthuser", password="pass")
        user_four_account = UserAccount.objects.create(user=user_four, username_slug = models.SlugField )
        user_four_account.save()

        response = self.client.get(reverse('other:viewAllUsers'))
        self.assertContains(response, user_one_account)
        self.assertContains(response, user_two_account)
        self.assertContains(response, user_three_account)
        self.assertContains(response, user_four_account)

    def test_view_one_user(self):
        client = Client()
        user = User.objects.create(email="userone@mail.com",username="firstuser", password="pass")
        user_account = UserAccount.objects.create(user=user, username_slug = models.SlugField )
        user_account.save()

        user_two = User.objects.create(email="usertwp@mail.com",username="myusername", password="pass")
        user_two_account = UserAccount.objects.create(user=user_two, username_slug = models.SlugField )
        user_two_account.save()

        response = self.client.get(reverse('other:viewOneUser', args =[user_account.username_slug]))
        self.assertContains(response, user_account)
        self.assertNotContains(response, user_two_account)

