from __future__ import absolute_import, unicode_literals

from .base import *

# Disable debug mode
DEBUG = False
TEMPLATE_DEBUG = False

# Compress static files offline
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'URLS': [get_env_variable('ELASTICSEARCH_URL')],
        'INDEX': get_env_variable('ELASTICSEARCH_INDEX'),
        'TIMEOUT': 5000,
    },
}

AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

COMPRESS_URL = 'https://{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)
STATIC_URL = 'https://{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)
MEDIA_URL = 'https://{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)

# PostgreSQL (Recommended, but requires the psycopg2 library and Postgresql development headers)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT'),
        'CONN_MAX_AGE': 600,
    }
}

RAVEN_CONFIG = {
    'dsn': get_env_variable('RAVEN_DSN'),
}

INSTALLED_APPS = INSTALLED_APPS + (
    'wagtail.contrib.wagtailfrontendcache',
    'raven.contrib.django.raven_compat',
    'interactives_content',
)

WAGTAILFRONTENDCACHE = {
    'cloudflare': {
        'BACKEND': 'wagtail.contrib.wagtailfrontendcache.backends.CloudflareBackend',
        'EMAIL': get_env_variable('CLOUDFLARE_EMAIL'),
        'TOKEN': get_env_variable('CLOUDFLARE_TOKEN'),
    },
}

FAVICON_PATH = STATIC_URL + 'img/favicon.png'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': get_env_variable('REDIS_CACHE_ENDPOINT'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

IS_PRODUCTION = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
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
