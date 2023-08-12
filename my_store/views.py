
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
    template_name = "registration/signup.html"
    model = User
    form_class = forms.UserSignUpForm
    success_url = reverse_lazy("hello")

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


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


class CustomerRead(View):
    def get(self, request):
        customers = models.Customers.objects.all()
        return render(
            request,
            template_name="customers_read.html",
            context={"customers": customers},
        )


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "customer_update.html"
    model = models.Customers
    form_class = forms.CustomerUpdateForm
    success_url = reverse_lazy("hello")
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


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "customer_delete.html"
    model = models.Customers
    success_url = reverse_lazy("hello")
    permission_required = "my_store.delete_customers", "my_store.delete_user"

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #
    #     context = self.get_context_data(object=self.object)
    #     return self.render_to_response(context)
    def post(self, request, *args, **kwargs):
        # Set self.object before the usual form processing flow.
        # Inlined because having DeletionMixin as the first base, for
        # get_success_url(), makes leveraging super() with ProcessFormView
        # overly complex.
        self.object = self.get_object()
        print(self.object)
        print(dir(self.object))
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)