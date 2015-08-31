from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WP_IMPORTER_IMAGE_DOWNLOAD_DOMAINS = ('opencanada.centos', 'opencanada.org',
                                      'www.opencanada.org')
WP_IMPORTER_USER_PHOTO_URL_PATTERN = "http://opencanada.centos/wp-content/uploads/userphoto/{}"

WP_IMPORTER_ARTICLE_PHOTO_URL_PATTERN = "http://opencanada.centos/wp-content/uploads/{}"

IS_PRODUCTION = False

INSTALLED_APPS = INSTALLED_APPS + (
    'interactives_content',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'opencanada',
        'CONN_MAX_AGE': 600,
    }
}
