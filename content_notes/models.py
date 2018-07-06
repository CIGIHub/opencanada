from __future__ import absolute_import, division, unicode_literals

import logging
from uuid import uuid4

from django.db import models
from django.forms.widgets import HiddenInput
from django.utils.encoding import python_2_unicode_compatible
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, RichTextFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable

logger = logging.getLogger('OpenCanada.ArticleModels')


def get_uuid():
    return uuid4().hex


@python_2_unicode_compatible
class EndNote(Orderable):
    text = RichTextField()
    uuid = models.CharField(max_length=64, blank=True)
    article = ParentalKey(
        "articles.ArticlePage",
        null=True,
        on_delete=models.SET_NULL,
        related_name='endnote_links'
    )

    def __init__(self, *args, **kwargs):
        super(EndNote, self).__init__(*args, **kwargs)
        if not self.uuid:
            self.uuid = get_uuid()

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = get_uuid()
        super(EndNote, self).save()

    def __str__(self):
        return self.text

    panels = [
        RichTextFieldPanel('text'),
        FieldPanel('uuid', widget=HiddenInput),
    ]


class Citation(Orderable):
    text = RichTextField()
    article = ParentalKey(
        "articles.ArticlePage",
        related_name='citation_links'
    )

    def __str__(self):
        return self.text

    panels = [
        RichTextFieldPanel('text'),
    ]
