from Donuts.models import *

def my_cp(request):
    restaurants = Restaurant.objects.all()
    ctx = {
        'restaurants': restaurants,
    }

    return ctx