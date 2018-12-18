from Donuts.models import *

def my_cp(request):
    restaurants = Restaurant.objects.all()
    dishes = Dish.objects.all()
    ctx = {
        'restaurants': restaurants,
        'dishes': dishes
    }

    return ctx