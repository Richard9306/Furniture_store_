from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    LoginView,
)
from django.views.generic import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from my_store import forms, models
from verify_email.email_handler import send_verification_email

class HomeView(View):
    def get(self, request):
        return render(request, template_name="index.html")


class UserCreateView(CreateView):
    template_name = "registration/signup.html"
    model = User
    form_class = forms.UserSignUpForm
    success_url = reverse_lazy("home")


    def form_valid(self, form):
        if form.is_valid():
            inactive_user = send_verification_email(self.request, form)
            return inactive_user



class SubmittablePasswordChangeView(PasswordChangeView):
    form_class = forms.SubmittablePasswordChangeForm
    template_name = "registration/password_change.html"
    success_url = reverse_lazy("password_change_done")


class SubmittablePasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"


class SubmittablePasswordResetView(PasswordResetView):
    form_class = forms.SubmittablePasswordResetForm
    template_name = "registration/password_reset.html"
    success_url = reverse_lazy("password_reset_done")


class SubmittablePasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"


class SubmittablePasswordResetConfirmView(PasswordResetConfirmView):
    form_class = forms.SubmittableSetPasswordForm
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class SubmittablePasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"

class SubmittableLoginView(LoginView):
    form_class = forms.SubmittableAuthenticationForm
    template_name = "registration/login.html"


class SubmittableLogoutView(LogoutView):
    template_name = "registration/logout.html"




class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "customer_update.html"
    model = models.Customers
    form_class = forms.CustomerUpdateForm
    success_url = reverse_lazy("customer_update_done")
    permission_required = "my_store.change_customers"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.initial = {
            "first_name": self.object.user.first_name,
            "last_name": self.object.user.last_name,
            "email": self.object.user.email,
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.user.first_name = self.request.POST["first_name"]
        self.object.user.last_name = self.request.POST["last_name"]
        self.object.user.email = self.request.POST["email"]
        self.object.user.save()
        return super().post(request, **kwargs)


class CustomerUpdateDoneView(View):
    def get(self, request):
        return render(request, template_name="customer_update_done.html")


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "customer_delete.html"
    model = models.Customers
    success_url = reverse_lazy("customer_delete_done")
    permission_required = "my_store.delete_customers", "my_store.delete_user"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.user.delete()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class CustomerDeleteDoneView(View):
    def get(self, request):
        return render(request, template_name="customer_delete_done.html")