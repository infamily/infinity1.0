import os
from .base import *

# DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug


def debug():
    """
    returns True if DEBUG env is 1
    returns False if DEBUG env is 0
    returns True if DEBUG env is not established
    """
    debug_value = os.getenv("DEBUG", False)

    if debug_value:
        return bool(int(debug_value))
    return True

DEBUG = debug()

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# END DEBUG CONFIGURATION

# DATABASE CONFIGURATION

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DATABASE_NAME", ""),
        'USER': os.getenv("DATABASE_USER", ""),
        'PASSWORD': os.getenv("DATABASE_PASSWORD", ""),
        'HOST': os.getenv("DATABASE_HOST", "127.0.0.1"),
        'PORT': os.getenv("DATABASE_PORT", "")
    }
}

# END DATABASE CONFIGURATION

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@infty.xyz")

if DEBUG:
    # If debug is enabled this means we use the project locally
    # let's allow Django to display the letters in the console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # TOOLBAR CONFIGURATION
    # See:
    # http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup
    if 'debug_toolbar' not in INSTALLED_APPS:
        INSTALLED_APPS += (
            'debug_toolbar',
        )

    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    # http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
    INTERNAL_IPS = ('127.0.0.1',)
    # END TOOLBAR CONFIGURATION
else:
    ALLOWED_HOSTS = ['.infty.xyz']
    # Because we're using https
    # http://django-allauth.readthedocs.org/en/latest/configuration.html
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
    EMAIL_BACKEND = "sgbackend.SendGridBackend"
    SENDGRID_USER = os.getenv("SENDGRID_USER", "")
    SENDGRID_PASSWORD = os.getenv("SENDGRID_PASSWORD", "")

    # CACHE CONFIGURATION
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    }

    # Set the cache backend to select2
    SELECT2_CACHE_BACKEND = 'default'
    # END CACHE CONFIGURATION
