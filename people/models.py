from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, RichTextFieldPanel,
                                                StreamFieldPanel)
from wagtail.wagtailcore.models import Page

from .fields import BioField


@python_2_unicode_compatible
class ContributorListPage(Page):
    subpage_types = ['ContributorPage']

    @property
    def contributors(self):
        contributors = ContributorPage.objects.live().descendant_of(self).order_by('last_name', 'first_name')
        return contributors

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class ContributorPage(Page):
    first_name = models.CharField(max_length=255, blank=True, default="")
    last_name = models.CharField(max_length=255, blank=True, default="")
    nickname = models.CharField(max_length=1024, blank=True, default="")

    email = models.EmailField(blank=True, default="")
    twitter_handle = models.CharField(max_length=16, blank=True, default="")

    short_bio = models.TextField(blank=True, default="")
    long_bio = BioField(blank=True, default="")

    headshot = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def save(self, *args, **kwargs):
        self.title = "{} {}".format(self.first_name, self.last_name)
        self.slug = slugify(self.title)
        super(ContributorPage, self).save(*args, **kwargs)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def last_comma_first_name(self):
        return "{}, {}".format(self.last_name, self.first_name)

    def __str__(self):
        return "{} {} - {}".format(self.first_name, self.last_name, self.email)


ContributorPage.content_panels = [
    FieldPanel('first_name'),
    FieldPanel('last_name'),
    FieldPanel('email'),
    FieldPanel('twitter_handle'),
    RichTextFieldPanel('short_bio'),
    StreamFieldPanel('long_bio'),
]
