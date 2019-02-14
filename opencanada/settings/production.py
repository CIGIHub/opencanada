from __future__ import absolute_import, unicode_literals

from .base import *
import django_heroku

# Disable debug mode
DEBUG = False

SECURE_SSL_REDIRECT = True
PREPEND_WWW = False # TODO: Set to true for production

ALLOWED_HOSTS = [get_env_variable('ALLOWED_HOSTS')]

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.elasticsearch6',
        'URLS': [get_env_variable('FOUNDELASTICSEARCH_URL')],
        'INDEX': 'wagtail',
        'TIMEOUT': 60,
        'OPTIONS': {},
        'INDEX_SETTINGS': {},
    }
}

AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATIC_URL = get_env_variable('STATIC_URL')
MEDIA_URL = get_env_variable('STATIC_URL')
AWS_S3_CUSTOM_DOMAIN = get_env_variable('AWS_S3_CUSTOM_DOMAIN')

# Compress static files offline
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True
COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_URL = STATIC_URL

RAVEN_CONFIG = {
    'dsn': get_env_variable('RAVEN_DSN'),
}

INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
    # 'interactives_content',
    'caching',
)

WAGTAILFRONTENDCACHE = {
    'cloudflare': {
        'BACKEND': 'wagtail.contrib.frontend_cache.backends.CloudflareBackend',
        'EMAIL': get_env_variable('CLOUDFLARE_EMAIL'),
        'TOKEN': get_env_variable('CLOUDFLARE_TOKEN'),
        'ZONEID': get_env_variable('CLOUDFLARE_ZONE_ID'),
    },
}

FAVICON_PATH = STATIC_URL + 'img/favicon.png'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': get_env_variable('REDIS_URL'),
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
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.template': {
            'level': 'WARNING',
            'handlers': ['sentry', 'console'],
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

ADMIN_ENABLED = False

django_heroku.settings(
    locals(),
    allowed_hosts=False,
    logging=False,
    secret_key=False,
    staticfiles=False,
    test_runner=False
)
