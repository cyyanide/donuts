from django import forms
from django.forms import ModelForm, DateInput
import datetime

from Donuts.models import *


class AddRestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        exclude = ['owner']

class AddDishForm(ModelForm):
    class Meta:
        model = Dish
        exclude = ['restaurant']


class DatePicker(DateInput):
    input_type = 'date'

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        exclude = ['who']
        widgets = {
            'date': DatePicker(),
        }

    def clean(self):

        cleaned_data = super().clean()

        date = cleaned_data.get('date')
        date_today = datetime.date.today()
        print (date, date_today)
        print(date<date_today)

        if date < date_today:
            self.add_error('date', "Choose correct date!")

        return cleaned_data


class AddUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField()
    surname = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput)

    def clean(self):

        cleaned_data = super().clean()

        field1 = cleaned_data.get('password')
        field2 = cleaned_data.get('repeat_password')

        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self.add_error("username", "This username is already in use!")

        if field1 != field2:
            self.add_error("repeat_password", "Confirm your password!")

        return cleaned_data

class LoginForm(forms.Form):
    login = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)

