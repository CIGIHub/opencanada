from __future__ import absolute_import

from wagtail.wagtailcore import hooks
from willow.backends.pillow import PillowBackend

from . import image_operations


@hooks.register('register_image_operations')
def register_image_operations():
    return [
        ('circle', image_operations.CircleOperation),
    ]


@PillowBackend.register_operation('putalpha')
def putalpha(backend, alpha):
    backend.image.putalpha(alpha)
