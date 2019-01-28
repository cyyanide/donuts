from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    who = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    booking_time_start = models.TimeField(verbose_name='Booking time')
    booking_time_end = models.TimeField(verbose_name='Booking end')
    people = models.IntegerField()


class Dish(models.Model):
    dish_name = models.CharField(max_length=64)
    dish_description = models.CharField(max_length=128)
    price = models.IntegerField()
    restaurant = models.ManyToManyField(Restaurant)
    dish_picture = models.ImageField(null=True, blank=True)
