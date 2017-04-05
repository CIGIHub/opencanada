from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '172.31.9.139']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

IS_PRODUCTION = False

INSTALLED_APPS = INSTALLED_APPS + (
    'interactives_content',
)

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch2',
        'INDEX': get_env_variable('ELASTICSEARCH_INDEX'),
        'TIMEOUT': 5000,
        # This setting will not work as intended with the ElasticSearch provided by http://www.searchly.com/
        # 'ATOMIC_REBUILD': True,
        'HOSTS': [{
            'host': get_env_variable('ELASTICSEARCH_HOST'),
            'port': get_env_variable('ELASTICSEARCH_PORT'),
            'http_auth': (get_env_variable('ELASTICSEARCH_USER'), get_env_variable('ELASTICSEARCH_PASSWORD')),
            'use_ssl': True,
            'verify_certs': False,
        }]
    },
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
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
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
    },
}
