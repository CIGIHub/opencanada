from __future__ import absolute_import, unicode_literals

from .base import *
import django_heroku

# Disable debug mode
# DEBUG = True
# DEBUG_PROPAGATE_EXCEPTIONS = True

# Compress static files offline
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
# COMPRESS_OFFLINE = True

# WAGTAILSEARCH_BACKENDS = {
#     'default': {
#         'BACKEND': 'wagtail.search.backends.elasticsearch2',
#         'INDEX': get_env_variable('ELASTICSEARCH_INDEX'),
#         'TIMEOUT': 5000,
#         # This setting will not work as intended with the ElasticSearch provided by http://www.searchly.com/
#         # 'ATOMIC_REBUILD': True,
#         'HOSTS': [{
#             'host': get_env_variable('ELASTICSEARCH_HOST'),
#             'port': get_env_variable('ELASTICSEARCH_PORT'),
#             'http_auth': (get_env_variable('ELASTICSEARCH_USER'), get_env_variable('ELASTICSEARCH_PASSWORD')),
#             'use_ssl': True,
#             'verify_certs': False,
#         }]
#     },
# }
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.db',
    },
}

AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")
#
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#
COMPRESS_URL = get_env_variable('STATIC_URL')
STATIC_URL = get_env_variable('STATIC_URL')
MEDIA_URL = get_env_variable('STATIC_URL')
AWS_S3_CUSTOM_DOMAIN = get_env_variable('AWS_S3_CUSTOM_DOMAIN')

# RAVEN_CONFIG = {
#     'dsn': get_env_variable('RAVEN_DSN'),
# }

INSTALLED_APPS = INSTALLED_APPS + (
    'wagtail.contrib.frontend_cache',
    # 'raven.contrib.django.raven_compat',
    # 'interactives_content',
    'caching',
)

# WAGTAILFRONTENDCACHE = {
#     'cloudflare': {
#         'BACKEND': 'wagtail.contrib.frontend_cache.backends.CloudflareBackend',
#         'EMAIL': get_env_variable('CLOUDFLARE_EMAIL'),
#         'TOKEN': get_env_variable('CLOUDFLARE_TOKEN'),
#         'ZONEID': get_env_variable('CLOUDFLARE_ZONE_ID'),
#     },
# }

FAVICON_PATH = STATIC_URL + 'img/favicon.png'

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': get_env_variable('REDIS_CACHE_ENDPOINT'),
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }

IS_PRODUCTION = True

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'root': {
#         'level': 'WARNING',
#         'handlers': ['sentry'],
#     },
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s '
#                       '%(process)d %(thread)d %(message)s'
#         },
#     },
#     'handlers': {
#         'sentry': {
#             'level': 'WARNING',
#             'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose'
#         }
#     },
#     'loggers': {
#         'django.template': {
#             'level': 'WARNING',
#             'handlers': ['sentry', 'console'],
#             'propagate': False,
#         },
#         'django.db.backends': {
#             'level': 'ERROR',
#             'handlers': ['console'],
#             'propagate': False,
#         },
#         'raven': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#             'propagate': False,
#         },
#         'sentry.errors': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#             'propagate': False,
#         },
#     },
# }
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
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
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
        # 'raven': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        #     'propagate': False,
        # },
        # 'sentry.errors': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        #     'propagate': False,
        # },
    },
}

# ADMIN_ENABLED = False

# ALLOWED_HOSTS = [get_env_variable('ALLOWED_HOSTS')]
ALLOWED_HOSTS = ['*'] # TODO: Fix this

django_heroku.settings(locals())
