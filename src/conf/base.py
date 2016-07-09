"""Common settings and globals."""


from os.path import abspath, basename, dirname, join, normpath
from sys import path
from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

import dj_database_url

# PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
if DJANGO_ROOT not in path:
    path.append(DJANGO_ROOT)
if join(DJANGO_ROOT, 'apps') not in path:
    path.append(join(DJANGO_ROOT, 'apps'))
# END PATH CONFIGURATION


# DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Your Name', 'your_email@example.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# END MANAGER CONFIGURATION


# DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASE_URL = "sqlite:///%s" % normpath(join(DJANGO_ROOT, 'default.db'))
DATABASES = {}
DATABASES['default'] = dj_database_url.config(default=DATABASE_URL)

# END DATABASE CONFIGURATION


# GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'America/Los_Angeles'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = None
BASE_DOMAIN = 'infty.xyz'
MAIN_DOMAIN = _('infty.xyz')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
#   ('ja', _('Japanese')),
#   ('fr', _('French')),
    ('zh-hans', _('Chinese')),
#   ('de', _('German')),
    ('lt', _('Lithuanian')),
#   ('uk', _('Ukrainian'))
    ('hr', _('Croatian')),
    ('ja', _('Japanese')),
)

LANGUAGES_DOMAINS = {
    #'infty.xyz': 'en',
    'sumanymai.lt': 'lt',
    'nsiku.com': 'zh-hans',
}

import os
LOCALE_PATHS = (
    os.path.join(DJANGO_ROOT, 'locale'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# END GENERAL CONFIGURATION


# MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
# END MEDIA CONFIGURATION


# STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See:
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(DJANGO_ROOT, 'static')),
)

# See:
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)
# END STATIC FILE CONFIGURATION

# BOWER CONFIGURATIONS
BOWER_COMPONENTS_ROOT = os.path.join(SITE_ROOT, 'components')

BOWER_PATH = '/usr/local/bin/bower'

BOWER_INSTALLED_APPS = [
    'bootstrap#3.3.6',
    'bootstrap-datepicker#1.6.0',
    'bootstrap-horizon#0.1.0',
    'bootswatch#3.3.6+1',
    'fancybox#2.1.5',
    'font-awesome#4.5.0',
    'jquery#2.2.0',
    'jquery-migrate#1.3.0',
    'jquery-ui#1.11.4',
]
# END BOWER CONFIGURATIONS

# SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = r"fvxomh%ce$ff77c)v=d7m+ranwi(yyyky&y1em!1_h1ak$09()"
# END SECRET CONFIGURATION


# SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
# END SITE CONFIGURATION


# FIXTURE CONFIGURATION
# See:
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(SITE_ROOT, 'fixtures')),
)
# END FIXTURE CONFIGURATION

# TEMPLATE CONFIGURATION
# See:
# https://docs.djangoproject.com/en/1.9/ref/templates/upgrading/#the-templates-settings


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            normpath(join(DJANGO_ROOT, 'templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'django.core.context_processors.request',

                'constance.context_processors.config',
                'core.context_processors.language_domains',
            ],
            'debug': DEBUG,
        },
    },
]
# END TEMPLATE CONFIGURATION


# MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
DJANGO_MIDDLEWARE_CLASSES = (
    # Default Django middleware.
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)
# END MIDDLEWARE CONFIGURATION


# URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'urls'
# END URL CONFIGURATION


# APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
)

DJANGO_APPS += (
    # Additional apps
    'django_extensions',
    'pure_pagination',
    'crispy_forms',
    'constance',
    'constance.backends.database',
    'storages',
    'autofixture',
    'django_select2',
    'django_markdown',
    'djmoney_rates',
    'djangobower',
    'rest_framework',
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}

# DEBUG-specific apps
if DEBUG:
    DJANGO_APPS += (
        'debug_toolbar',
    )


# LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'log/project/infty.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# END LOGGING CONFIGURATION

CRISPY_TEMPLATE_PACK = "bootstrap3"

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'


# WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'
# END WSGI CONFIGURATION


# AUTHORISATION/AUTHENTICATION CONFIGURATION
# account-related apps
DJANGO_APPS += (
    'avatar',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
)

# Allauth providers
DJANGO_APPS += (
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin',
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# Removed from new module
# http://django-allauth.readthedocs.org/en/latest/changelog.html#from-0-21-0
# TEMPLATE_CONTEXT_PROCESSORS += (
#     "allauth.account.context_processors.account",
#     "allauth.socialaccount.context_processors.socialaccount",
# )

# auth and allauth settings
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_PASSWORD_MIN_LENGTH = 3
ACCOUNT_ADAPTER = 'invitation.models.InvitationsAdapter'
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_FORMS = {'login': 'users.forms.LoginForm'}

# djmoney_rates
DJANGO_MONEY_RATES = {
    'DEFAULT_BACKEND': 'djmoney_rates.backends.OpenExchangeBackend',
    'OPENEXCHANGE_URL': 'https://openexchangerates.org/api/latest.json',
    'OPENEXCHANGE_APP_ID': '4d6a086f4e904ce787b649ead3d67215',
    'OPENEXCHANGE_BASE_CURRENCY': 'USD',
}

# hour value ( api.stlouisfed.org )
FRED_KEY = '0a90ca7b5204b2ed6e998d9f6877187e'
FRED_SERIES = 'CES0500000003'

# GOOGLE TRANSLATE API KEY
GOOGLE_TRANSLATE_API_KEY = 'AIzaSyCgzrDm1HPL0a1t-j55sPTCYi5wwlqlpB4'

# END AUTHORISATION/AUTHENTICATION CONFIGURATION

# GEOIP2 LIBRARY FILES
GEOIP_PATH = join(SITE_ROOT, 'conf/geoip2data/')
GEOIP_COUNTRY = 'GeoLite2-Country.mmdb'
GEOIP_CITY = 'GeoLite2-City.mmdb'

SUBSCRIBE_SUCCESS_REDIRECT_URL = '/'

DATE_FORMAT = 'Y-m-d'
SHORT_DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i'

# APP CONFIGURATION
from .app import LOCAL_APPS
from .app import LOCAL_MIDDLEWARE_CLASSES

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS
# END APP CONFIGURATION

MIDDLEWARE_CLASSES = DJANGO_MIDDLEWARE_CLASSES + LOCAL_MIDDLEWARE_CLASSES

# App settings have bigger priority
from .app import *
