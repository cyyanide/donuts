from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import *
# from .forms import *

class RestaurantsView(View):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        return render(request, 'donuts/listAllRestaurants.html', {'restaurants': restaurants})

class ShowMenuView(View): # and details!
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        return render(request, 'donuts/showMenu.html', {'restaurant': restaurant})






