"""
Django settings for Oscar_Site project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from oscar.defaults import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ylwq%_f_9p&o*2j@q+8a9c8g7+(jam$)r-neyt5jug^$=24&sh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

from oscar import get_core_apps

INSTALLED_APPS = [
                     'django.contrib.admin',
                     'django.contrib.auth',
                     'django.contrib.contenttypes',
                     'django.contrib.sessions',
                     'django.contrib.messages',
                     'django.contrib.staticfiles',

                     'django.contrib.sites',
                     'django.contrib.flatpages',

                     'compressor',
                     # 3rd-party apps that oscar depends on
                     'widget_tweaks',
                     'crispy_forms',

                     # 'smart_load_tag',

                     'allauth',
                     'allauth.account',
                     'allauth.socialaccount',
                     # ... include the providers you want to enable:
                     'allauth.socialaccount.providers.google',
                     # 'allauth.socialaccount.providers.facebook',

                     # 'customer',
                     # template tags app
                     'apps.user',

                 ] + get_core_apps(['apps.catalogue',
                                    'apps.partner',
                                    'apps.offer',
                                    # 'apps.customer',
                                    ])

SITE_ID = 1

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = not DEBUG

# auth user model setting
AUTH_USER_MODEL = 'user.User'

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '314332771646-p85nrbtk6dl1ocrqpm2uaomf6omsd61j.apps.googleusercontent.com',
            'secret': 'UGpFdUhNphd2jKSa3KSthCo3',
            'key': ''
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    'oscar.apps.customer.auth_backends.EmailBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

ROOT_URLCONF = 'Oscar_Site.urls'

from oscar import OSCAR_MAIN_TEMPLATE_DIR

location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', x)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            location('templates'),
            OSCAR_MAIN_TEMPLATE_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                # `allauth` needs this from django
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # oscar setting
                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',

            ],
        },
    },
]

WSGI_APPLICATION = 'Oscar_Site.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eoscar_site_db',
        'USER': 'pradnya',
        'PASSWORD': 'girish',
        # 'HOST': '',
        # 'POST': '',
        'ATOMIC_REQUESTS': True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# OSCAR_USE_LESS = True
TEMPLATE_DEBUG = True
THUMBNAIL_DEBUG = True

# allauth setting
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'

# ACCOUNT_SIGNUP_REDIRECT = 'users_app.utils.custom_signup_redirect'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
# not working auto_signup, if the user already signed in Google account,
# then also show Google form to take credentials, but its auto Signing same as AUto_Signup=True
# if the True, takes username and password provided by Google, and skips Local Signup Form fillup
# if False, Local Signup Form should be filled again
SOCIALACCOUNT_AUTO_SIGNUP = False

ACCOUNT_FORMS = {
    'signup': 'apps.user.forms.signup_form.SignupForm',
}

ACCOUNT_ADAPTER = 'apps.user.adapters.signup_adapter.SignupAdapter'

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True

ACCOUNT_EMAIL_VERIFICATION = "none"

from django.urls import reverse_lazy

LOGIN_REDIRECT_URL = OSCAR_HOMEPAGE
LOGOUT_REDIRECT_URL = OSCAR_HOMEPAGE

# Oscar Setting goes here
# OSCAR_USE_LESS = True
OSCAR_SHOP_NAME = 'Orgatma'
OSCAR_SHOP_TAGLINE = 'A site for shopping Organic Foods to customer'

OSCAR_DEFAULT_CURRENCY = 'INR'

OSCAR_CURRENCY_FORMAT = {
    'INR': {
        'currency_digits': False,
        'format_type': "accounting",
        'format': u'Rs #,##0',
    },
    # 'EUR': {
    #     'format': u'#,##0\xa0¤',
    # }
}
