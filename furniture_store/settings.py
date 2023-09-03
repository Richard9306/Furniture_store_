"""
Django settings for furniture_store project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
for item in os.environ:
    print(item)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
load_dotenv()

SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#SMTP Configuration
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('PASSWORD_USER')
PASSWORD_RESET_TIMEOUT_DAYS = 1
DEFAULT_FROM_EMAIL = f'noreply <{EMAIL_HOST_USER}>'
print('Email:', EMAIL_HOST_USER)
print('Password:', EMAIL_HOST_PASSWORD)
print(SECRET_KEY)

# Application definition
INSTALLED_APPS = [
    "my_store",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "verify_email.apps.VerifyEmailConfig",
    "dotenv",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "furniture_store.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "furniture_store.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        # "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "NAME": "my_store.my_validators.my_password_validators.MyUserAttributeSimilarityValidator",
    },
    {
        # "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "NAME": "my_store.my_validators.my_password_validators.MyMinimumLengthValidator",
    },
    {
        # "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        "NAME": "my_store.my_validators.my_password_validators.MyCommonPasswordValidator",
    },
    {
        # "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        "NAME": "my_store.my_validators.my_password_validators.MyNumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "pl"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

#verify_email settings:
# LOGIN_URL = 'login'
VERIFICATION_SUCCESS_TEMPLATE = None
SUBJECT = 'Weryfikacja adresu email'
HTML_MESSAGE_TEMPLATE = "registration/my_custom_verification_msg.html"

THOUSAND_SEPARATOR = ' '
USE_THOUSAND_SEPARATOR = True