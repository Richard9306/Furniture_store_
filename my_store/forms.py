from django.contrib.auth.forms import UserCreationForm
from django import forms
from my_store import models
from django.contrib.auth.models import User

class UserSignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        # first_name = forms.CharField(max_length=30)
        # last_name = forms.CharField(max_length=60)
        # email = forms.EmailField()