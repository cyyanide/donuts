from django.db import models

class Menu(models.Model):
    restaurant_name = models.CharField(max_length=64)

class Dish(models.Model):
    dish_name = models.CharField(max_length=64)
    dish_description = models.CharField(max_length=128)
    price = models.IntegerField()
    menu = models.ManyToManyField(Menu)

class Restaurant(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    menu = models.OneToOneField(Menu, on_delete=models.CASCADE, primary_key=True)

class Booking(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

