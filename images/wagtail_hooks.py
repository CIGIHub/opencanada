from __future__ import absolute_import

import logging

from PIL import ImageDraw
from wagtail.wagtailcore import hooks
from willow.backends.pillow import PillowBackend

from . import image_operations

logger = logging.getLogger(__name__)


@hooks.register('register_image_operations')
def register_image_operations():
    return [
        ('circle', image_operations.CircleOperation),
        ('rcircle', image_operations.CircleWithRingOperation),
    ]


@PillowBackend.register_operation('putalpha')
def putalpha(backend, alpha):
    try:
        backend.image.putalpha(alpha)
    except ValueError as e:
        # Log exception but return and don't apply the operation.
        logger.exception(e)
        return


@PillowBackend.register_operation('draw_bitmap')
def draw_bitmap(backend, bitmap, fill):
    image = ImageDraw.Draw(backend.image)
    image.bitmap((0, 0), bitmap, fill)
