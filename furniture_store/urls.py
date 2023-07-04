"""
URL configuration for furniture_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from my_store import views
from django.contrib.auth.views import LoginView
from django_registration import backends

change_password = "change_password"
urlpatterns = [
    path("admin/", admin.site.urls),
    path(r'^accounts/', include('registration.backends.hmac.urls')),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout/", views.SubmittableLogoutView.as_view(), name="logout"),
    path("accounts/registration", views.UserCreateView.as_view(), name="registration"),
    path("accounts/password_change", views.SubmittablePasswordChangeView.as_view(), name="password_change"),
    path("accounts/password_change_done", views.SubmittablePasswordChangeDoneView.as_view(), name="password_change_done"),
    path("hello", views.HomeView.as_view(), name="hello"),
    path("customers/read", views.CustomerRead.as_view(), name="customers_read"),
    path("customers/create", views.CustomerCreateView.as_view(), name="customer_create"),
    path("customers/update/<pk>", views.CustomerUpdateView.as_view(), name="customer_update"),
    path("customers/delete/<pk>", views.CustomerDeleteView.as_view(), name="customer_delete"),
    path("customers/user_to_customer_create", views.UserToCustomerCreateView.as_view(), name="user_to_customer_create")
]
