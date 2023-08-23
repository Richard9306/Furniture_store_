from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm,
    AuthenticationForm,
    UsernameField, PasswordResetForm, SetPasswordForm,
)
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from my_store import models
from django.contrib.auth.models import User
import datetime


class UserSignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["email", "username"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Podany adres email jest już zajęty.")
        return email
    def clean_username(self):
        """Reject usernames that differ only in case."""
        username = self.cleaned_data.get("username")
        if username and self._meta.model.objects.filter(username__iexact=username).exists():
            raise ValidationError("Podany login jest już zajęty.")
        return username

    username = UsernameField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Login*", "autofocus": True}
        ),
        help_text="Dozwolona ilość znaków to: 150. Tylko litery, cyfry i @/./+/-/_.",
        error_messages=""
    )

    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Adres email*"}
        ),
        required=True
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
        label="Imie:",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )
    last_name = forms.CharField(
        label="Nazwisko:",
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True,
    )
    email = forms.EmailField(
        label="Adres email:",
        widget=forms.HiddenInput(
            attrs={
                "class": "form-control",
                "readonly": "readonly",
                }
        ),
        required=True,
    )

    phone_nr = forms.CharField(
        max_length=15,
        label="Nr kontaktowy:",
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True,
    )

    TODAY = datetime.datetime.today().date()
    birth_date = forms.DateField(
        label="Data urodzenia:",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "max": TODAY,
                "type": "date"
            }
        ),
        required=True,
    )
    country = forms.CharField(
        max_length=60,
        label="Kraj",
        widget=forms.HiddenInput(
            attrs={
                "class": "form-control",
                "readonly": "readonly",
            }
        ),
        initial="Polska",
        required=True,
    )
    city = forms.CharField(
        max_length=45,
        label="Miasto:",
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True,
    )
    postal_code = forms.CharField(
        max_length=6,
        label="Kod pocztowy",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "00-000"}
        ),
        validators=[
            RegexValidator(
                regex=r"\d{2}-\d{3}",
                message="Niepoprawny format kodu pocztowego.",
            ),
        ],
        required=True,
    )
    street = forms.CharField(
        max_length=75,
        label="Ulica:",
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True,
    )
    house_nr = forms.CharField(
        max_length=10,
        label="Nr domu:",
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True,
    )
    flat_nr = forms.IntegerField(
        label="Nr mieszkania(opcjonalnie):",
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False,
    )
