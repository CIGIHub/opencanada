from __future__ import absolute_import, division, unicode_literals

from .utils import CustomTemplateChecker, TemplateDoesNotExist
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
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
            self._override_block_templates(self.theme)
            custom_template = "{}/{}".format(self.theme.folder, original_template)
            return custom_template
        else:
            return original_template

    def _override_block_templates(self, theme):
        if theme:
            checker = CustomTemplateChecker()
            iterables = [x for x in self.__dict__.values() if hasattr(x, '__getitem__')]
            for iterable in iterables:
                for item in iterable:
                    if hasattr(item, 'block'):
                        try:
                            original_template_name = item.block.meta.template
                            custom_template_name = "{}/{}".format(theme.folder, original_template_name)
                            checker.get_absolute_path(custom_template_name)
                            item.block.meta.template = custom_template_name
                        except AttributeError:
                            # Block does not define its own template...
                            pass
                        except TemplateDoesNotExist:
                            # Custom template for the Block does not exist...
                            pass

    style_panels = [
        MultiFieldPanel(
            [
                SnippetChooserPanel('theme', Theme),
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
