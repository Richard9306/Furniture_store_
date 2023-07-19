from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm,
    AuthenticationForm,
    UsernameField, PasswordResetForm, SetPasswordForm,
)
from django import forms
from django.core.validators import RegexValidator

from my_store import models
from django.contrib.auth.models import User


class UserSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username"]

    username = UsernameField(
        label="*Pola obowiązkowe",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Login*", "autofocus": True}
        ),
        help_text="Dozwolona ilość znaków to: 150. Tylko litery, cyfry i @/./+/-/_.",
    )
    password1 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "new-password",
                "placeholder": "Hasło*",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "new-password",
                "placeholder": "Powtórz hasło*",
            }
        ),
        strip=False,
        help_text="",
    )
    first_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    last_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    email = forms.EmailField(widget=forms.HiddenInput(), required=False)
    phone_nr = forms.CharField(widget=forms.HiddenInput(), required=False)
    birth_date = forms.DateField(widget=forms.HiddenInput(), required=False)
    country = forms.CharField(
        widget=forms.HiddenInput(), initial="Polska", required=False
    )
    city = forms.CharField(widget=forms.HiddenInput(), required=False)
    postal_code = forms.CharField(widget=forms.HiddenInput(), required=False)
    street = forms.CharField(widget=forms.HiddenInput(), required=False)
    house_nr = forms.CharField(widget=forms.HiddenInput(), required=False)
    flat_nr = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    error_messages = {
        "password_mismatch": "Podane hasła różnią się !",
        "unique": "Wybrany login jest już zajęty.",
    }

    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)
        phone_nr = self.cleaned_data["phone_nr"]
        birth_date = self.cleaned_data["birth_date"]
        country = self.cleaned_data["country"]
        city = self.cleaned_data["city"]
        postal_code = self.cleaned_data["postal_code"]
        street = self.cleaned_data["street"]
        house_nr = self.cleaned_data["house_nr"]
        flat_nr = self.cleaned_data["flat_nr"]
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
            attrs={
                "class": "form-control",
                "autocomplete": "current-password",
                "autofocus": True,
                "placeholder": "Dotychczasowe hasło",
            }
        ),
    )
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nowe hasło",
                "autocomplete": "new-password",
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Powtórz nowe hasło",
                "autocomplete": "new-password",
            }
        ),
    )


class SubmittableAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Login", "autofocus": True}
        ),
    )
    password = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Hasło",
                "autocomplete": "current-password",
            }
        ),
    )
    error_messages = {
        "invalid_login": "Niepoprawny login lub hasło. Zwróć uwagę na wielkość liter.",
        "inactive": "Konto nieaktywne.",
    }


class SubmittablePasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "E-mail*"}
        ),
        required=True,
    )

class SubmittableSetPasswordForm(SetPasswordForm):

    error_messages = {
        "password_mismatch": "Podane hasła różnią się !",
    }
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nowe hasło",
                "autocomplete": "new-password",
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Powtórz nowe hasło",
                "autocomplete": "new-password",
            }
        ),
    )

class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Customers
        fields = [
            "user",
            "first_name",
            "last_name",
            "email",
            "phone_nr",
            "birth_date",
            "country",
            "city",
            "postal_code",
            "street",
            "house_nr",
            "flat_nr",
        ]

        widgets = {"user": forms.HiddenInput()}

    first_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Imię*"}),
        required=True,
    )
    last_name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nazwisko*"}
        ),
        required=True,
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "E-mail*"}
        ),
        required=True,
    )
    phone_nr = forms.CharField(
        max_length=15,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nr telefonu(+48)*"}
        ),
        required=True,
    )
    birth_date = forms.DateField(
        label="",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Data urodzenia(rrrr-mm-dd)*",
            }
        ),
        required=True,
    )
    country = forms.CharField(
        max_length=60,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Kraj*",
                "readonly": "readonly",
            }
        ),
        initial="Polska",
        required=True,
    )
    city = forms.CharField(
        max_length=45,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Miasto*"}
        ),
        required=True,
    )
    postal_code = forms.CharField(
        max_length=6,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Kod pocztowy(xx-xxx)*"}
        ),
        validators=[
            RegexValidator(
                regex=r"\d{2}-\d{3}",
                message="Poprawny format dla kodu pocztowego to: xx-xxx",
            ),
        ],
        required=True,
    )
    street = forms.CharField(
        max_length=75,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ulica*"}
        ),
        required=True,
    )
    house_nr = forms.CharField(
        max_length=10,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nr domu*"}
        ),
        required=True,
    )
    flat_nr = forms.IntegerField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nr lokalu(opcjonalnie)"}
        ),
        required=False,
    )
