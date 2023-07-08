from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, LoginView

from django.views.generic import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.contrib.auth.models import User
from my_store import forms, models
from my_store.models import Customers


class HomeView(View):
    def get(self, request):
        return render(request, template_name="index.html")

class UserCreateView(CreateView):
    template_name = "registration.html"
    model = User
    form_class = forms.UserSignUpForm
    success_url = reverse_lazy("hello")


class SubmittablePasswordChangeView(PasswordChangeView):
    form_class = forms.SubmittablePasswordChangeForm
    template_name = "password_change.html"
    success_url = reverse_lazy("password_change_done")

class SubmittablePasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "password_change_done.html"

class SubmittablePasswordResetView(PasswordResetView):
    template_name = "password_reset.html"
    success_url = reverse_lazy("password_reset_confirm")

class SubmittablePasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"

class SubmittablePasswordResetDoneView(PasswordResetDoneView):
    template_name = "password_reset_done.html"

class SubmittableLogoutView(LogoutView):
    template_name = "logout.html"

class CustomerRead(View):
    def get(self, request):
        customers = models.Customers.objects.all()
        return render(request, template_name="customers_read.html", context={"customers": customers})


class CustomerCreateView(CreateView):
    template_name = "customer_create.html"
    model = models.Customers
    form_class = forms.CustomerForm
    success_url = reverse_lazy("customers_read")

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "customer_update.html"
    model = models.Customers
    form_class = forms.CustomerForm
    success_url = reverse_lazy("customers_read")
    permission_required = "my_store.change_customers"

    def bound_form(request, id):
        customer = Customers.objects.get(id=id)
        form = forms.CustomerForm(initial={"name": customer.phone_nr})
        return render(request, template_name="customer_update.html", context={"form": form})

class CustomerDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = "customer_delete.html"
    model = models.Customers
    success_url = reverse_lazy("customers_read")
    permission_required = "my_store.delete_customers", "my_store.delete_user"

class UserToCustomerCreateView(LoginRequiredMixin,CreateView):
    template_name = "user_to_customer_create.html"
    model = models.Customers
    form_class = forms.UserToCustomerForm
    success_url = reverse_lazy("customers_read")

class SubmittableLoginView(LoginView):
    form_class = forms.SubmittableAuthenticationForm
    template_name = "registration/login.html"
