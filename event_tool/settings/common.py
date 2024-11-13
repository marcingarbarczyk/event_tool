"""
Django settings for event_tool project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from ast import literal_eval
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('EVENT_TOOL_SECRETKEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = literal_eval(os.environ.get('EVENT_TOOL_DEBUG', 'True'))

ALLOWED_HOSTS = os.environ.get('EVENT_TOOL_ALLOWED_HOSTS').split(',')

CSRF_COOKIE_DOMAIN = (
    os.environ.get('EVENT_TOOL_CSRF_COOKIE_DOMAIN') if os.environ.get('EVENT_TOOL_CSRF_COOKIE_DOMAIN') else None
)
CSRF_TRUSTED_ORIGINS = (
    os.environ.get('EVENT_TOOL_CSRF_TRUSTED_ORIGINS').split(',')
    if os.environ.get('EVENT_TOOL_CSRF_TRUSTED_ORIGINS')
    else []
)

# Application definition

BASE_URL = os.environ.get('EVENT_TOOL_BASE_URL')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'easy_thumbnails',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'rest_framework.authtoken',
    'compressor',
    # APPS
    'utils',
    'apps.events',
    'apps.dynamo_forms',
    'apps.script_manager',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SITE_ID = 1

ROOT_URLCONF = 'event_tool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'event_tool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_DBHOST'),
        'PORT': os.environ.get('POSTGRES_DBPORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get('EVENT_TOOL_STATIC_ROOT'))

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '../node_modules/@fortawesome/fontawesome-free'),
    os.path.join(BASE_DIR, '../node_modules/glightbox/dist'),
    os.path.join(BASE_DIR, '../node_modules/vanilla-lazyload/dist'),
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, os.environ.get('EVENT_TOOL_MEDIA_ROOT'))

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CKEDITOR

CKEDITOR_UPLOAD_PATH = 'media/'
CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
    },
}


# Email settings

EMAIL_BACKEND = os.environ.get('EVENT_TOOL_EMAIL_BACKEND')

EMAIL_HOST = os.environ.get('EVENT_TOOL_EMAIL_HOST')

EMAIL_PORT = os.environ.get('EVENT_TOOL_EMAIL_PORT')

EMAIL_HOST_USER = os.environ.get('EVENT_TOOL_EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = os.environ.get('EVENT_TOOL_EMAIL_HOST_PASSWORD')

EMAIL_USE_SSL = literal_eval(os.environ.get('EVENT_TOOL_EMAIL_USE_SSL', 'False'))

DEFAULT_FROM_EMAIL = os.environ.get('EVENT_TOOL_DEFAULT_FROM_EMAIL')

NEW_REGISTRATIONS_EMAIL_RECEIVERS = os.environ.get('EVENT_TOOL_NEW_REGISTRATIONS_EMAIL_RECEIVERS').split(',')


# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# Compressor

COMPRESS_ROOT = BASE_DIR / 'static'
COMPRESS_ENABLED = True

# Tpay debug URLS (ngrok)

TPAY_DEBUG_RESULT_URL = os.environ.get('TPAY_DEBUG_RESULT_URL')
TPAY_DEBUG_RETURN_URL = os.environ.get('TPAY_DEBUG_RETURN_URL')
