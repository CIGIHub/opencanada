'''
Setting to be used to support the admin.opencanada.org domain which exclusively
provides editing.
'''
from __future__ import absolute_import, unicode_literals

from .production import *

ROOT_URLCONF = 'opencanada.urls_admin'

PREPEND_WWW = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Explicitly use database
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.db',
    }
}

IS_PRODUCTION = False
ADMIN_ENABLED = True

SITE_ID = 2
