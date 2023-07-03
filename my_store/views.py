from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
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
    template_name = "registration.html"
    form_class = forms.CustomerForm
    success_url = reverse_lazy("hello")
    model = User

class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = "change_password.html"
    success_url = reverse_lazy("password_change_done")