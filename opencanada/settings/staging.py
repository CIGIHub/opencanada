from __future__ import absolute_import, unicode_literals

from .production import *

ALLOWED_HOSTS = [get_env_variable('ALLOWED_HOSTS')]

ROOT_URLCONF = 'opencanada.urls_admin'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Explicitly use database
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.db',
    }
}

COMPRESS_URL = 'https://staging-files.opencanada.org/'
STATIC_URL = 'https://staging-files.opencanada.org/'
MEDIA_URL = 'https://staging-files.opencanada.org/'
AWS_S3_CUSTOM_DOMAIN = 'staging-files.opencanada.org'

IS_PRODUCTION = False
ADMIN_ENABLED = True

SITE_ID = 3
