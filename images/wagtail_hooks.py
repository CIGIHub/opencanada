from __future__ import absolute_import

from PIL import ImageDraw
from wagtail.wagtailcore import hooks
from willow.backends.pillow import PillowBackend

from . import image_operations


@hooks.register('register_image_operations')
def register_image_operations():
    return [
        ('circle', image_operations.CircleOperation),
        ('ringed_circle', image_operations.CircleWithRingOperation),
    ]


@PillowBackend.register_operation('putalpha')
def putalpha(backend, alpha):
    backend.image.putalpha(alpha)


@PillowBackend.register_operation('draw_bitmap')
def draw_bitmap(backend, bitmap, fill):
    image = ImageDraw.Draw(backend.image)
    image.bitmap((0, 0), bitmap, fill)
