from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# https://gist.github.com/NotSqrt/5f3c76cd15e40ef62d09
class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

MIGRATION_MODULES = DisableMigrations()
