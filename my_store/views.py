
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, LoginView
from django.contrib.auth import login
from django.views.generic import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from my_store import forms, models


class HomeView(View):
    def get(self, request):
        return render(request, template_name="index.html")

class UserCreateView(CreateView):
    template_name = "registration.html"
    model = User
    form_class = forms.UserSignUpForm
    success_url = reverse_lazy("hello")

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


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

class SubmittableLoginView(LoginView):
    form_class = forms.SubmittableAuthenticationForm
    template_name = "registration/login.html"

class SubmittableLogoutView(LogoutView):
    template_name = "logout.html"

class CustomerRead(View):
    def get(self, request):
        customers = models.Customers.objects.all()
        curr_user = request.user.id
        return render(request, template_name="customers_read.html", context={"customers": customers, "curr_user": curr_user})


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "customer_update.html"
    model = User
    form_class = forms.CustomerUpdateForm
    success_url = reverse_lazy("customers_read")
    permission_required = "my_store.change_customers"
    # def form_valid(self, form):
    #     if self.object:
    #         return self.request.user


class CustomerDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = "customer_delete.html"
    model = models.Customers
    success_url = reverse_lazy("customers_read")
    permission_required = "my_store.delete_customers", "my_store.delete_user"


