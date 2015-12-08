from __future__ import absolute_import, division, unicode_literals

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
    contact_email = models.EmailField(blank=True, null=True, help_text="Only provide if this should be different from the site default email contact address.")

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


@python_2_unicode_compatible
class TwitterUser(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    twitter_handle = models.CharField(max_length=16)
    biography = models.CharField(max_length=255)

    def __str__(self):
        return self.twitter_handle

    class Meta:
        abstract = True


@python_2_unicode_compatible
class TwitteratiMemberCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TwitteratiMember(TwitterUser):
    category = models.ForeignKey(TwitteratiMemberCategory)


class TwitteratiMixin(object):
    @property
    def twitterati_categories(self):
        return TwitteratiMemberCategory.objects.all()

    @property
    def twitterati_members(self):
        return TwitteratiMember.objects.all()

    @property
    def sorted_twitterati_members(self):
        return TwitteratiMember.objects.order_by('category', 'first_name')

    @property
    def sorted_twitterati_members_by_category(self):
        members = self.sorted_twitterati_members
        ordered_categories = []
        members_by_category = {}
        for member in members:
            category_name = member.category.name
            if not members_by_category.has_key(category_name):
                members_by_category[category_name] = []
                ordered_categories.append(category_name)
            members_by_category[category_name].append(member)
        sorted_members_by_category = []
        for category_name in ordered_categories:
            sorted_members_by_category.append(members_by_category[category_name])
        return sorted_members_by_category

