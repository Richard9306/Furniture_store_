from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, LogoutView
import re
from django.views.generic import FormView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from my_store import forms, models
# Create your views here.

class HelloView(View):
    def get(self, request):
        return render(request, template_name="hello.html")

class UserCreateView(CreateView):
    template_name = "accounts/registration.html"
    model = User
    form_class = forms.UserSignUpForm
    success_url = reverse_lazy("hello")


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("password_change_done")

class SubmittablePasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"
class SubmittableLogoutView(LogoutView):
    template_name = "accounts/logout.html"

class CustomerRead(View):
    def get(self, request):
        customers = models.Customers.objects.all()

        return render(request, template_name="customers_read.html", context={"customers": customers})

# print(dir(models.Customers.objects.all()[0].user))
class CustomerCreateView(CreateView):
    template_name = "customer_create.html"
    model = models.Customers
    form_class = forms.CustomerForm
    success_url = reverse_lazy("customers_read")

class CustomerUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = "customer_update.html"
    model = models.Customers
    form_class = forms.CustomerForm
    success_url = reverse_lazy("customers_read")
    permission_required = "my_store.change_customers"

class CustomerDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = "customer_delete.html"
    model = models.Customers
    success_url = reverse_lazy("customers_read")
    permission_required = "my_store.delete_customers"
