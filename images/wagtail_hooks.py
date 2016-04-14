from __future__ import absolute_import

from wagtail.wagtailcore import hooks
from . import image_operations


@hooks.register('register_image_operations')
def register_image_operations():
    return [
        ('circlecrop', image_operations.CircleCropOperation),
        # ('circle', image_operations.CircleOperation),
        # ('rcircle', image_operations.CircleWithRingOperation),
    ]
