from django.contrib.auth.forms import UserCreationForm
from django import forms
from my_store import models
from django.contrib.auth.models import User
from django.db.transaction import atomic

class UserSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email"]

class UserToCustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customers
        fields = "__all__"
class CustomerForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    phone_nr = forms.CharField(max_length=15)
    birth_date = forms.DateField(widget=forms.SelectDateWidget)
    country = forms.CharField(max_length=60)
    city = forms.CharField(max_length=45)
    postal_code = forms.CharField(max_length=6)
    street = forms.CharField(max_length=75)
    house_nr = forms.CharField(max_length=10)
    flat_nr = forms.IntegerField(widget=forms.NumberInput)
    @atomic
    def save(self, commit=True):
        self.instance.is_active = False
        result = super().save(commit)
        phone_nr = self.cleaned_data['phone_nr']
        birth_date = self.cleaned_data['birth_date']
        country = self.cleaned_data['country']
        city = self.cleaned_data['city']
        postal_code = self.cleaned_data['postal_code']
        street = self.cleaned_data['street']
        house_nr = self.cleaned_data['house_nr']
        flat_nr = self.cleaned_data['flat_nr']
        customer = models.Customers(
            phone_nr=phone_nr,
            birth_date=birth_date,
            country=country,
            city=city,
            postal_code=postal_code,
            street=street,
            house_nr=house_nr,
            flat_nr=flat_nr,
            user=result,
        )
        if commit:
            customer.save()
        return result