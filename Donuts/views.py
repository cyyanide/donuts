from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from Donuts.form import *
from .models import *
# from .forms import *

class RestaurantsView(View):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        return render(request, 'donuts/listAllRestaurants.html', {'restaurants': restaurants})

class ShowMenuView(View):
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        dishes = Dish.objects.filter(pk=restaurant_id)
        return render(request, 'donuts/showMenu.html', {'restaurant': restaurant,
                                                        'dishes': dishes})

class AddRestaurantView(View):
    def get(self, request):
        form = AddRestaurantForm()
        return render(request, 'donuts/addRestaurant.html', {'form': form})
    def post(self, request):
        restaurant = Restaurant()
        form = AddRestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
        return redirect('/')

class DeleteRestaurantView(View):
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        return render(request, 'donuts/deleteRestaurant.html', {'restaurant': restaurant})
    def post(self, request, restaurant_id):
        if request.POST.get('decision') == 'yes':
            Restaurant.objects.filter(pk=restaurant_id).first().delete()
            return HttpResponse("Dish has been deleted")
        elif request.POST.get('decision') == 'no':
            return redirect('/')

class AddDishView(View):
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        form = AddDishForm()
        return render(request, 'donuts/addMenu.html', {'form': form,
                                                       'restaurant': restaurant})
    def post(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        dish = Dish()
        form = AddDishForm(request.POST, instance=dish)
        if form.is_valid():
            form.save()
            dish.restaurant.add(restaurant)
        return redirect('/')

class DeleteDishView(View):
    def get(self, request, restaurant_id, dish_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        dish = Dish.objects.get(pk=dish_id)
        return render(request, 'donuts/deleteDish.html', {'restaurant': restaurant,
                                                          'dish': dish})
    def post(self, request, restaurant_id, dish_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        if request.POST.get('decision') == 'yes':
            Dish.objects.filter(pk=dish_id).first().delete()
            return HttpResponse("Dish has been deleted")
        elif request.POST.get('decision') == 'no':
            return redirect('/')

class BookingView(View):
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        form = BookingForm()
        return render(request, 'donuts/booking.html', {'form': form,
                                                       'restaurant': restaurant})
    def post(self, request):
        booking = Booking()
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
        return redirect('/')



















