from __future__ import absolute_import, unicode_literals

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from wagtail.wagtailimages.models import (AbstractImage, AbstractRendition,
                                          Image)


class AttributedImage(AbstractImage):
    credit = models.CharField(max_length=1024, blank=True, default="")
    source = models.CharField(max_length=1024, blank=True, default="")
    usage_restrictions = models.TextField(blank=True, default="")

    admin_form_fields = Image.admin_form_fields + (
        "source",
        "credit",
        "usage_restrictions",
    )


class AttributedRendition(AbstractRendition):
    image = models.ForeignKey(AttributedImage, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


# Delete the source image file when an image is deleted
@receiver(pre_delete, sender=AttributedImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Delete the rendition image file when a rendition is deleted
@receiver(pre_delete, sender=AttributedRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)
