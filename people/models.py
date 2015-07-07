from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from wagtail.wagtailadmin.edit_handlers import FieldPanel, RichTextFieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


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
    long_bio = models.TextField(blank=True, default="")

    headshot = models.ForeignKey(
        'images.AttributedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.title = "{} {}".format(self.first_name, self.last_name)
        elif self.first_name:
            self.title = self.first_name
        elif self.last_name:
            self.title = self.last_name
        elif self.nickname:
            self.title = self.nickname
        else:
            self.title = ""
        self.slug = slugify(self.title)
        if self.twitter_handle and not self.twitter_handle.startswith("@"):
            self.twitter_handle = "@{}".format(self.twitter_handle)
        super(ContributorPage, self).save(*args, **kwargs)

        if not self.slug:
            self.title = str(self.id)
            self.slug = slugify(self.title)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def last_comma_first_name(self):
        return "{}, {}".format(self.last_name, self.first_name)

    @property
    def display_twitter_handle(self):
        if self.twitter_handle:
            return self.twitter_handle[1:]
        return self.twitter_handle

    def __str__(self):
        return "{} {} - {}".format(self.first_name, self.last_name, self.email)


ContributorPage.content_panels = [
    FieldPanel('first_name'),
    FieldPanel('last_name'),
    FieldPanel('email'),
    FieldPanel('twitter_handle'),
    RichTextFieldPanel('short_bio'),
    RichTextFieldPanel('long_bio'),
    ImageChooserPanel('headshot'),
]
