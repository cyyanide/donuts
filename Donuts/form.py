import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, URLValidator
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from Donuts.models import *


class AddRestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'

class AddDishForm(ModelForm):
    class Meta:
        model = Dish
        exclude = ['restaurant']

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        # widgets = {
        #     'date': forms.DateField(initial=datetime.date.today),
        # }
