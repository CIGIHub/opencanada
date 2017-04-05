from __future__ import absolute_import, unicode_literals

from .production import *

ALLOWED_HOSTS = [get_env_variable('ALLOWED_HOSTS')]

ROOT_URLCONF = 'opencanada.urls_admin'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

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

COMPRESS_URL = 'https://staging-files.opencanada.org/'
STATIC_URL = 'https://staging-files.opencanada.org/'
MEDIA_URL = 'https://staging-files.opencanada.org/'
AWS_S3_CUSTOM_DOMAIN = 'staging-files.opencanada.org'

IS_PRODUCTION = False
ADMIN_ENABLED = True

SITE_ID = 3
