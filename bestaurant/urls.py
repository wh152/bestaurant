"""bestaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import LoginView
import accounts.views as acc_views
import search.views as search_views

urlpatterns = [
    path('', search_views.index, name='index'),
    path('admin/', admin.site.urls),
    path('', include('other.urls')),
    path('accounts/register/', acc_views.register, name="register"),
    path('accounts/login/', acc_views.user_login, name="login"),
    path('accounts/description/change/', acc_views.change_description, name='change_description'),
    path('accounts/description/change/done/', acc_views.change_description_done, name='change_description_done'),
    path('accounts/image/change/', acc_views.change_image, name='change_image'),
    path('accounts/image/change/done/', acc_views.change_image_done, name='change_image_done'),
    path('accounts/', include('registration.backends.simple.urls')),
    # path('accounts/google/login/', LoginView.as_view()),
    path('accounts/', include('allauth.urls')),
    path('search/', include('search.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
