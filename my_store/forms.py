from django.contrib.auth.forms import UserCreationForm
from django import forms
from my_store import models
class CustomerForm(UserCreationForm):

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=60)
    email = forms.EmailField()
    # birth_date = forms.DateField()
    # phone_nr = forms.CharField(max_length=9)
    # country = forms.CharField(max_length=60)
    # city = forms.CharField(max_length=45)
    # postal_code = forms.CharField(max_length=5)
    # street = forms.CharField(max_length=75)
    # house_nr = forms.CharField(max_length=10)
    # flat_nr = forms.IntegerField()