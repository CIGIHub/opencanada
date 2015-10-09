'''
Setting to be used to support the admin.opencanada.org domain which exclusively
provides editing.
'''
from __future__ import absolute_import, unicode_literals

from .production import *

ROOT_URLCONF = 'opencanada.urls_admin'

ADMIN_ENABLED = True

SITE_ID = 2
