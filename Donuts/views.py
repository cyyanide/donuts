from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from Donuts.form import *
from .models import *


class RestaurantsView(View):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        return render(request, 'donuts/listAllRestaurants.html', {'restaurants': restaurants})


class ShowMenuView(View):
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        dishes = Dish.objects.filter(pk=restaurant_id)
        return render(request, 'donuts/showMenu2.html', {'restaurant': restaurant,
                                                         'dishes': dishes})


class AddRestaurantView(View):
    def get(self, request):
        form = AddRestaurantForm()
        return render(request, 'donuts/addRestaurant.html', {'form': form})

    def post(self, request):
        restaurant = Restaurant()
        form = AddRestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            new_restaurant = form.save(commit=False)
            new_restaurant.owner = request.user
            new_restaurant.save()
        return redirect('/controlpanel/%s' % restaurant.pk)


class AddDishView(View):
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        form = AddDishForm()
        return render(request, 'donuts/addMenu.html', {'form': form,
                                                       'restaurant': restaurant})

    def post(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        dish = Dish()
        form = AddDishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()
            dish.restaurant.add(restaurant)
        return redirect('/')


class BookingView(View):
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        form = BookingForm()
        return render(request, 'donuts/booking.html', {'form': form,
                                                       'restaurant': restaurant})

    def post(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        booking = Booking()
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            new_booking = form.save(commit=False)
            new_booking.who = request.user
            new_booking.save()
        return render(request, 'donuts/bookingSummary.html', {'booking': booking,
                                                              'form': form})


class DeleteRestaurantView(View):
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        if request.user == restaurant.owner:
            return render(request, 'donuts/deleteRestaurant.html', {'restaurant': restaurant})
        else:
            return HttpResponse("Permission denied! You do not have access to manage this restaurant")

    def post(self, request, restaurant_id):
        if request.POST.get('decision') == 'yes':
            Restaurant.objects.filter(pk=restaurant_id).first().delete()
            return HttpResponse("Restaurant has been deleted")
        elif request.POST.get('decision') == 'no':
            return redirect('/')


class DeleteDishView(View):
    def get(self, request, restaurant_id, dish_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        dish = Dish.objects.get(pk=dish_id)
        if request.user == restaurant.owner:
            return render(request, 'donuts/deleteDish.html', {'restaurant': restaurant,
                                                              'dish': dish})
        else:
            return HttpResponse("Permission denied! You do not have access to manage this restaurant")

    def post(self, request, restaurant_id, dish_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        if request.POST.get('decision') == 'yes':
            Dish.objects.filter(pk=dish_id).first().delete()
            return HttpResponse("Dish has been deleted")
        elif request.POST.get('decision') == 'no':
            return redirect('/')


class RegisterView(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, "donuts/addUser.html", {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            email = form.cleaned_data.get('email')
            User.objects.create_user(username=username, password=password, email=email, first_name=name,
                                     last_name=surname)
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
            return redirect('/')
        return render(request, "donuts/addUser.html", {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'donuts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('login'),
                                password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse('Wrong login or password!')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class AllBookingsView(View):
    def get(self, request, restaurant_id):
        bookings = Booking.objects.filter(restaurant=restaurant_id)
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        return render(request, 'donuts/allBookings.html', {'bookings': bookings,
                                                           'restaurant': restaurant})


def restaurant_data_validation(request, restaurant):
    name = request.POST.get("name")
    description = request.POST.get("description")
    opening_time = request.POST.get("opening_time")
    closing_time = request.POST.get("closing_time")
    restaurant.name = name
    restaurant.description = description
    restaurant.opening_time = opening_time
    restaurant.closing_time = closing_time
    if name and description and opening_time and closing_time:
        restaurant.save()


class RestaurantControlPanelView(View):
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        form = AddRestaurantForm(instance=restaurant)
        dishes = Dish.objects.filter(pk=restaurant_id)
        if request.user == restaurant.owner:
            return render(request, 'donuts/restoControlPanel.html', {'restaurant': restaurant,
                                                                     'dishes': dishes,
                                                                     'form': form})
        else:
            return HttpResponse("Permission denied! You do not have access to manage this restaurant")

    def post(self, request, restaurant_id):
        restaurant_data_validation(request, Restaurant.objects.get(pk=restaurant_id))
        return HttpResponse("Changes have been applied")


class MyBookingView(View):
    def get(self, request, who_id):
        bookings = Booking.objects.filter(pk=who_id)
        who = User.objects.filter(pk=who_id)
        return render(request, 'donuts/myBookings.html', {'bookings': bookings,
                                                          'who': who})


class LearnMoreView(View):
    def get(self, request):
        return render(request, 'donuts/learnMore.html')
