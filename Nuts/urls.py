"""Nuts URL Configuration

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
from django.urls import path
from django.conf.urls import url
from django.views.static import serve

from Donuts.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', RestaurantsView.as_view()),
    url(r'^menu/(?P<restaurant_id>(\d)+)$', ShowMenuView.as_view()),
    url(r'^addrestaurant$', AddRestaurantView.as_view()),
    url(r'^adddish/(?P<restaurant_id>(\d)+)$', AddDishView.as_view()),
    url(r'^controlpanel/deletedish/(?P<restaurant_id>(\d)+)/(?P<dish_id>(\d)+)$', DeleteDishView.as_view()),
    url(r'^deleterestaurant/(?P<restaurant_id>(\d)+)$', DeleteRestaurantView.as_view()),
    url(r'^book/(?P<restaurant_id>(\d)+)$', BookingView.as_view()),
    url(r'^register$', RegisterView.as_view()),
    url(r'^login$', LoginView.as_view()),
    url(r'^logout$', LogoutView.as_view()),
    url(r'^bookings/(?P<restaurant_id>(\d)+)$', AllBookingsView.as_view()),
    url(r'^controlpanel/(?P<restaurant_id>(\d)+)$', RestaurantControlPanelView.as_view()),
    url(r'^mybooking/(?P<who_id>(\d)+)$', MyBookingView.as_view()),
    url(r'^more', LearnMoreView.as_view()),

]

# w trybie debug możemy dodać ten adres do naszych ścieżek url
if settings.DEBUG:
    urlpatterns.append(url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))
