from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()


class Dish(models.Model):
    dish_name = models.CharField(max_length=64)
    dish_description = models.CharField(max_length=128)
    price = models.IntegerField()
    restaurant = models.ManyToManyField(Restaurant)

