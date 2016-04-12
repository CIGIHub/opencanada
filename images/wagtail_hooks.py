from __future__ import absolute_import

import logging

from wagtail.wagtailcore import hooks

from . import image_operations

logger = logging.getLogger(__name__)


@hooks.register('register_image_operations')
def register_image_operations():
    return [
        ('circle', image_operations.CircleOperation),
        ('rcircle', image_operations.CircleWithRingOperation),
    ]
