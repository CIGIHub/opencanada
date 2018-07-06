from __future__ import absolute_import, unicode_literals

from django.db import models
from wagtail.images.models import (AbstractImage, AbstractRendition,
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
    image = models.ForeignKey(
        AttributedImage,
        related_name='renditions',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
