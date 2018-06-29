from __future__ import absolute_import, division, unicode_literals

import itertools

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel)
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from .blocks import ThemeableStructBlock


def get_default_theme_object():
    return Theme.objects.filter(is_default=True).order_by('id').first()


def get_default_theme():
    theme = get_default_theme_object()
    return theme.id


@python_2_unicode_compatible
class ThemeContent(ClusterableModel):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(blank=True, null=True,
                                      help_text="Only provide if this should be different from the site default email contact address.")

    panels = [
        FieldPanel('name'),
        FieldPanel('contact_email'),
        InlinePanel('block_links', label="Content Blocks"),
        InlinePanel('follow_links', label="Follow Links"),
        InlinePanel('logo_links', label="Logos"),
    ]

    def __str__(self):
        return self.name

register_snippet(ThemeContent)


@python_2_unicode_compatible
class Theme(models.Model):
    name = models.CharField(max_length=1024)
    folder = models.CharField(max_length=1024, default="themes/default")
    is_default = models.BooleanField(default=False)
    content = models.ForeignKey(ThemeContent, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('folder'),
        FieldPanel('is_default'),
        SnippetChooserPanel('content'),
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

    def serve(self, request, *args, **kwargs):
        from articles.fields import ChapterField
        if self.theme:
            # If a theme is set, 'Push' the theme down to the blocks, if possible
            for field in self._meta.fields:
                # Each StreamField and ChapterField should have a StreamBlock
                if not isinstance(field, StreamField) and not isinstance(field, ChapterField):
                    continue

                stream_block = field.stream_block
                if not isinstance(stream_block, StreamBlock):
                    continue

                if isinstance(field, ChapterField):
                    ordered_blocks = itertools.chain(
                        stream_block.child_blocks.values(),
                        stream_block.child_blocks['chapter'].child_blocks['body'].child_blocks.values()
                    )
                else:
                    # Assuming that each StreamBlock has an ordered dict of child Blocks
                    ordered_blocks = stream_block.child_blocks.values()
                for block in ordered_blocks:
                    # We only need to set the Theme for blocks that support themes
                    if isinstance(block, ThemeableStructBlock):
                        block.set_theme(self.theme)

        return super(ThemeablePage, self).serve(request, *args, **kwargs)

    def get_template(self, request, *args, **kwargs):
        original_template = super(ThemeablePage, self).get_template(request, *args, **kwargs)
        if self.theme:
            custom_template = "{}/{}".format(self.theme.folder, original_template)
            return custom_template
        else:
            return original_template

    style_panels = [
        MultiFieldPanel(
            [
                SnippetChooserPanel('theme'),
            ],
            heading="Theme"
        ),
    ]


@python_2_unicode_compatible
class TextBlock(models.Model):
    name = models.CharField(max_length=255)
    usage = models.CharField(max_length=255, blank=True, default="")
    heading = models.TextField(blank=True, default="")
    content = RichTextField(blank=True, default="")

    panels = [
        FieldPanel('name'),
        FieldPanel('heading'),
        FieldPanel('content'),
        FieldPanel('usage'),
    ]

    def __str__(self):
        return self.name

register_snippet(TextBlock)


@python_2_unicode_compatible
class FollowLink(models.Model):
    name = models.CharField(max_length=255)
    usage = models.CharField(max_length=255, blank=True, default="")
    link = models.CharField(max_length=1024)

    panels = [
        FieldPanel('name'),
        FieldPanel('link'),
        FieldPanel('usage'),
    ]

    def __str__(self):
        return self.name

register_snippet(FollowLink)


@python_2_unicode_compatible
class LogoBlock(models.Model):
    name = models.CharField(max_length=255)
    usage = models.CharField(max_length=255, blank=True, default="")
    logo = models.ForeignKey(
        'images.AttributedImage',
        on_delete=models.CASCADE
    )
    link = models.CharField(max_length=2048, blank=True, null=True)

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('logo'),
        FieldPanel('link'),
        FieldPanel('usage'),
    ]

    def __str__(self):
        return self.name

register_snippet(LogoBlock)


class ContentBlockLink(models.Model):
    block = models.ForeignKey(
        "TextBlock",
        related_name='content_links',
        on_delete=models.CASCADE
    )
    theme_content = ParentalKey(
        "ThemeContent",
        related_name='block_links'
    )

    panels = [SnippetChooserPanel("block")]


class ContentFollowLink(models.Model):
    block = models.ForeignKey(
        "FollowLink",
        related_name='content_links',
        on_delete=models.CASCADE
    )
    theme_content = ParentalKey(
        "ThemeContent",
        related_name='follow_links'
    )

    panels = [SnippetChooserPanel("block")]


class ContentLogoLink(models.Model):
    block = models.ForeignKey(
        "LogoBlock",
        related_name='content_links',
        on_delete=models.CASCADE
    )
    theme_content = ParentalKey(
        "ThemeContent",
        related_name='logo_links'
    )

    panels = [SnippetChooserPanel("block")]
