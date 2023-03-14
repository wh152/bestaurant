import os
import json
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bestaurant.settings')

import django
django.setup()
from accounts.models import *
from search.models import *
from django.core.files import File
from django.core.files.images import ImageFile
from django.template.defaultfilters import slugify
from PIL import Image


def populate():
    populate_accounts()
    populate_restaurants()
    populate_advertisements()
    populate_reviews()
    populate_categories()


def populate_accounts():
    accounts = read_data("accounts")

    for account in accounts:
        username = account["username"]
        username_slug = slugify(username) 
        email = account["email"]
        password = account["password"]
        restaurantOwner = account["restaurantOwner"]
        about = account["about"]
        photo = get_image_path("profile_images", username, account["photo"])

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        user_account = UserAccount.objects.create(user=user, username_slug=username_slug,
                                                restaurantOwner=restaurantOwner, about=about)

        if photo:
            photo_file = upload_image("profile_images", username)
            photo_name = username_slug + ".jpg"
            user_account.photo.save(photo_name, photo_file)
            photo_file.close()

        user_account.save()

    default_image =Image.open(os.path.join(settings.BASE_DIR, "population_data", "profile_images", "default.jpg"))
    default_image.save(os.path.join(settings.MEDIA_DIR, "profile_images", "default.jpg"))

    
def populate_restaurants():
    restaurants = read_data("restaurants")

    for restaurant in restaurants:
        owner = UserAccount.objects.get(user=User.objects.get(username=restaurant["owner"]))
        restaurantName = restaurant["restaurantName"]
        restaurantNameSlugged = slugify(restaurantName)
        category = restaurant["category"]
        address = restaurant["address"]
        logo = get_image_path("restaurant_logos", restaurantNameSlugged, restaurant["logo"])

        restaurant = Restaurant.objects.create(owner=owner, restaurantName=restaurantName,
                                                restaurantNameSlugged=restaurantNameSlugged, 
                                                category=category, address=address)

        if logo:
            logo_file = upload_image("restaurant_logos", restaurantName)
            logo_name = restaurantNameSlugged + ".jpg"
            restaurant.logo.save(logo_name, logo_file)
            logo_file.close()

        restaurant.save()


def populate_advertisements():
    advertisements = read_data("advertisements")

    for advertisement in advertisements:
        restaurantName = advertisement["restaurant"]
        restaurantNameSlugged = slugify(restaurantName)
        restaurant = Restaurant.objects.get(restaurantName=restaurantName)
        description = advertisement["description"]
        advertImage = get_image_path("advertisement_images", restaurantNameSlugged, True)

        advertisement = Advertisement.objects.create(restaurant=restaurant, 
                                                    description=description)

        if advertImage:
            advert_file = upload_image("advertisement_images", restaurantName)
            advert_name = restaurantNameSlugged + ".jpg"
            advertisement.advertImage.save(advert_name, advert_file)
            advert_file.close()
            
        advertisement.save()


def populate_reviews():
    reviews = read_data("reviews")

    for review in reviews:
        reviewer = UserAccount.objects.get(user=User.objects.get(username=review["reviewer"]))
        restaurant = Restaurant.objects.get(restaurantName=review["restaurant"])
        rating = review["rating"]
        comment = review["comment"]

        review = Review.objects.create(reviewer=reviewer, restaurant=restaurant, 
                                        rating=rating, comment=comment)
        review.save()


def populate_categories():
    for category in ["Casual Dining", "Fine Dining", "Fast Food", "Cafe", "Coffeehouse"]:
        Category.objects.create(name=category)


def read_data(filename):
    with open(os.path.join(settings.BASE_DIR, "population_data", filename+".json")) as f:
        return json.load(f)


def get_image_path(images_dir, image_name, image_exists):
    if image_exists:
        image_name += ".jpg"
        image_path = os.path.join(settings.BASE_DIR, "population_data", images_dir, image_name)
    else:
        image_path = None
    return image_path


def upload_image(image_dir, image_name):
    image_path = os.path.join(settings.BASE_DIR, "population_data", image_dir, image_name+".jpg")
    if not os.path.exists(image_path):
        image_path = "".join(image_path.split(".")[:-1] + [".jpeg"])
    image_file = open(image_path, "rb")
    return image_file


if __name__ == '__main__':
    print('Starting population script')
    populate()
    print('Finished population script')