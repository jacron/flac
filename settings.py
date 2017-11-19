"""
Django settings for flac project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nr-t^m#8-jxeak+-&3w05$!91l3s(h&40d8*!o5yev$b@2*sly'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'rest-framework',
    'flac',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flac.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + '/templates/',
            BASE_DIR + '/templatetags/'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'flac.templatetags.page_tags'
            ],
            # 'loaders': [
            #     ('django.template.loaders.cached.Loader', [
            #         'django.template.loaders.filesystem.Loader',
            #         'django.template.loaders.app_directories.Loader',
            #         # 'path.to.custom.Loader',
            #     ]),
            # ],
        },
    },
]
# TEMPLATE_DIRS = (
#     '/Users/orion/PycharmProjects/flac/venv/flac/flac/templates',
# )

WSGI_APPLICATION = 'flac.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DEFAULT_CHARSET = 'UTF-8'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
# https://stackoverflow.com/questions/10165638/django-isnt-serving-static-files-getting-404-errors
STATICFILES_DIRS = (os.path.join('static'),)

MEDIA_PLAYER = '/Applications/Media Center 21.app'
SQLITE3_FILE = 'venv/db.sqlite3'
COVER_FILE = '/folder.jpg'
BACK_FILE = '/back.jpg'
PERSON_FILE = '/person.jpg'
INSTRUMENTS_PATH = '/Volumes/Media/Audio/Klassiek/Instrumenten/'
COMPONIST_PATH = '/Volumes/Media/Audio/Klassiek/Componisten/'
PERFORMER_PATH = '/Volumes/Media/Audio/Klassiek/Performers/'
COVER_PATH = '/Volumes/Media/tmp/{}.jpg'
TMP_PATH = '/Volumes/Media/tmp'
SKIP_DIRS = ['website', 'artwork', 'Artwork', 'etc', 'scans', 'Scans', 'scan',
            'website boxset', '#Booklets', 'Pixels', 'Graphics', 'Info + Art', 'Art',
            'Covers', ]
