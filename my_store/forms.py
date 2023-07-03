from django.contrib.auth.forms import UserCreationForm
from django import forms
from my_store import models
from django.contrib.auth.models import User

class UserSignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customers
        fields = "__all__"