from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '172.31.9.139']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

IS_PRODUCTION = False

INSTALLED_APPS = INSTALLED_APPS + (
    'interactives_content',
)

# Explicitly use database
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.db',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'opencanada',
        'CONN_MAX_AGE': 600,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },

    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },

    },
    'loggers': {
        'django.template': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
