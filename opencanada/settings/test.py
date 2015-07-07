from __future__ import absolute_import, unicode_literals

import os

from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WP_IMPORTER_IMAGE_DOWNLOAD_DOMAINS = ('',)
WP_IMPORTER_USER_PHOTO_URL_PATTERN = "file://" + os.path.join(PROJECT_ROOT,
                                                              "wordpress_importer",
                                                              "tests", "files",
                                                              "{}")
