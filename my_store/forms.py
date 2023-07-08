from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm, UsernameField
from django import forms
from django.contrib.auth.password_validation import NumericPasswordValidator

from my_store import models
from django.contrib.auth.models import User
from django.db.transaction import atomic

class UserSignUpForm(UserCreationForm):

    help_texts = {
        "min_length": "Twoje hasło musi składać się conajmniej z 8 znaków."
    }
    error_messages = {
        "password_mismatch": "Podane hasła nie są jednakowe."
    }
    password1 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password", "placeholder": "Hasło*"}),
        help_text=password_validation.password_validators_help_text_html(),
        # """Twoje hasło nie może być zbyt podobne do innych danych osobowych.
        #           Twoje hasło musi zawierać co najmniej 8 znaków.
        #           Twoje hasło nie może być powszechnie używanym hasłem.
        #           Twoje hasło nie może składać się wyłącznie z cyfr."""

    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password", "placeholder": "Powtórz hasło*"}),
        strip=False,
        help_text="",
    )
    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {
            "username": "*Pola obowiązkowe",
            "email": "",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Login*"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-mail*"}),
        }

        help_texts = {
            "username": "Dozwolona ilość znaków to: 150. Tylko litery, cyfry i @/./+/-/_."
        }


class UserToCustomerForm(forms.ModelForm):

    class Meta:
        model = models.Customers
        fields = "__all__"
class CustomerForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

        labels = {
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "",
        }

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Login*"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Imię*"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nazwisko*"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-mail*"}),
        }

        help_texts = {
            "username": "Dozwolona ilość znaków: 150. Tylko litery, cyfry i @/./+/-/_."
        }

        error_messages = {

        }
    phone_nr = forms.CharField(max_length=15, label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nr telefonu(+48)*"}))
    birth_date = forms.DateField(label="", widget=forms.DateInput(attrs={"class": "form-control", "placeholder": "Data urodzenia(rrrr-mm-dd)*"}))
    country = forms.CharField(max_length=60, label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Kraj*"}))
    city = forms.CharField(max_length=45, label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Miasto*"}))
    postal_code = forms.CharField(max_length=6, label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Kod pocztowy(xx-xxx)*"}))
    street = forms.CharField(max_length=75, label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ulica*"}))
    house_nr = forms.CharField(max_length=10, label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nr domu*"}))
    flat_nr = forms.IntegerField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nr lokalu(opcjonalnie)"}), required=False)

    password1 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "new-password", "placeholder": "Hasło*"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "new-password", "placeholder": "Powtórz hasło*"}),
        strip=False,
        help_text="",
    )
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

class SubmittablePasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "current-password", "autofocus": True, "placeholder": "Dotychczasowe hasło"}
        ),
    )
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Nowe hasło", "autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Nowe hasło", "autocomplete": "new-password"}),
    )

class SubmittableAuthenticationForm(AuthenticationForm):
    username = UsernameField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Login", "autofocus": True}))
    password = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Hasło", "autocomplete": "current-password"}),
    )
