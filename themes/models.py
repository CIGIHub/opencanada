from __future__ import absolute_import, division, unicode_literals

from basic_site.models import UniquelySlugable
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


def get_default_theme_object():
    return Theme.objects.filter(is_default=True).order_by('id').first()


def get_default_theme():
    theme = get_default_theme_object()
    return theme.id


@python_2_unicode_compatible
class BackgroundImageBlock(UniquelySlugable):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        'images.AttributedImage',
    )
    position = models.CharField(max_length=2048, blank=True, null=True, help_text='For example: top center')

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('image'),
        FieldPanel('position'),
    ]

    def __str__(self):
        return self.name

register_snippet(BackgroundImageBlock)


@python_2_unicode_compatible
class ThemeContent(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(blank=True, null=True, help_text="Only provide if this should be different from the site default email contact address.")

    panels = [
        FieldPanel('name'),
        FieldPanel('contact_email'),
        InlinePanel('block_links', label="Content Blocks"),
        InlinePanel('follow_links', label="Follow Links"),
        InlinePanel('logo_links', label="Logos"),
        InlinePanel('backgroundImage_links', label="Background Images"),
    ]

    def __str__(self):
        return self.name

register_snippet(ThemeContent)


@python_2_unicode_compatible
class Theme(models.Model):
    name = models.CharField(max_length=1024)
    folder = models.CharField(max_length=1024, default="themes/default")
    is_default = models.BooleanField(default=False)
    content = models.ForeignKey(ThemeContent, null=True)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('folder'),
        FieldPanel('is_default'),
        SnippetChooserPanel('content', ThemeContent),
    ]

register_snippet(Theme)


class ThemeablePage(Page):
    is_creatable = False

    class Meta:
        abstract = True

    theme = models.ForeignKey(Theme,
                              default=get_default_theme,
                              on_delete=models.SET_NULL,
                              null=True)

    def get_template(self, request, *args, **kwargs):
        original_template = super(ThemeablePage, self).get_template(request, *args, **kwargs)
        if self.theme:
            return "{}/{}".format(self.theme.folder, original_template)
        else:
            return original_template

    style_panels = [
        MultiFieldPanel(
            [
                SnippetChooserPanel('theme', Theme),
            ],
            heading="Theme"
        ),
    ]


@python_2_unicode_compatible
class TextBlock(UniquelySlugable):
    name = models.CharField(max_length=255)
    heading = models.TextField(blank=True, default="")
    content = RichTextField(blank=True, default="")

    panels = [
        FieldPanel('name'),
        FieldPanel('heading'),
        FieldPanel('content'),
    ]

    def __str__(self):
        return self.name

register_snippet(TextBlock)


@python_2_unicode_compatible
class FollowLink(UniquelySlugable):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=1024)

    panels = [
        FieldPanel('name'),
        FieldPanel('link'),
    ]

    def __str__(self):
        return self.name

register_snippet(FollowLink)


@python_2_unicode_compatible
class LogoBlock(UniquelySlugable):
    name = models.CharField(max_length=255)
    logo = models.ForeignKey(
        'images.AttributedImage',
    )
    link = models.CharField(max_length=2048, blank=True, null=True)

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('logo'),
        FieldPanel('link'),
    ]

    def __str__(self):
        return self.name

register_snippet(LogoBlock)


class ContentBlockLink(models.Model):
    block = models.ForeignKey(
        "TextBlock",
        related_name='content_links'
    )
    theme_content = ParentalKey(
        "ThemeContent",
        related_name='block_links'
    )

    panels = [SnippetChooserPanel("block", TextBlock)]


class ContentFollowLink(models.Model):
    block = models.ForeignKey(
        "FollowLink",
        related_name='content_links'
    )
    theme_content = ParentalKey(
        "ThemeContent",
        related_name='follow_links'
    )

    panels = [SnippetChooserPanel("block", FollowLink)]


class ContentLogoLink(models.Model):
    block = models.ForeignKey(
        "LogoBlock",
        related_name='content_links'
    )
    theme_content = ParentalKey(
        "ThemeContent",
        related_name='logo_links'
    )

    panels = [SnippetChooserPanel("block", LogoBlock)]


class ContentBackgroundImageLink(models.Model):
    block = models.ForeignKey(
        "BackgroundImageBlock",
        related_name='content_links'
    )
    theme_content = ParentalKey(
        "ThemeContent",
        related_name='backgroundImage_links'
    )

    panels = [SnippetChooserPanel("block", BackgroundImageBlock)]
