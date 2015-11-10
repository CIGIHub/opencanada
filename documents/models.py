from __future__ import absolute_import, unicode_literals

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtaildocs.models import (Document)


class AttributedDocument(Document):
    credit = models.CharField(max_length=1024, blank=True, default="", verbose_name=_('Credit'))
    source = models.CharField(max_length=1024, blank=True, default="", verbose_name=_('Source'))
    usage_restrictions = models.TextField(blank=True, default="", verbose_name=_('Usage Restrictions'))

    admin_form_fields = (
        'title',
        'file',
        'tags',
        'source',
        'credit',
        'usage_restrictions',
    )


# Delete the source image file when an image is deleted
@receiver(pre_delete, sender=AttributedDocument)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)
