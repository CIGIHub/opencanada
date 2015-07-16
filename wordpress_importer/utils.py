from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_setting(name):
    '''
    Precedence: environment variables, django settings
    '''
    name = 'WP_IMPORTER_{}'.format(name)

    value = os.environ.get(name)

    if value is not None:
        return value

    if hasattr(settings, name):
        return getattr(settings, name)

    raise ImproperlyConfigured(
        'Setting {} is required to be set either in the environment or settings.py'.format(name)
    )
