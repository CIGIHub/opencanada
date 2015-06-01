from __future__ import absolute_import, unicode_literals

from basic_site.models import BasePage
from django.db import models
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, RichTextFieldPanel,
                                                StreamFieldPanel)
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from people import models as people_models


class HomePage(Page):
    pass


class LegacyArticlePage(Page, BasePage):
    excerpt = models.TextField()
    author = models.ForeignKey(
        "people.Contributor",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


LegacyArticlePage.content_panels = Page.content_panels + [
    RichTextFieldPanel('body'),
    RichTextFieldPanel('excerpt'),
    SnippetChooserPanel('author', people_models.Contributor),
]


class ArticlePage(Page):
    subtitle = models.TextField(blank=True, default="")
    author = models.ForeignKey(
        "people.Contributor",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('Heading', blocks.CharBlock(classname="heading")),
        ('Text', blocks.RichTextBlock()),
        ('Image', ImageChooserBlock()),
        ('Embed', EmbedBlock()),
    ])


ArticlePage.content_panels = Page.content_panels + [
    FieldPanel('subtitle'),
    SnippetChooserPanel('author', people_models.Contributor),
    StreamFieldPanel('body'),
]

register_snippet(people_models.Contributor)

people_models.Contributor.panels = [
    FieldPanel('first_name'),
    FieldPanel('last_name'),
    FieldPanel('nickname'),
    FieldPanel('email'),
    FieldPanel('twitter_handle'),
    RichTextFieldPanel('short_bio'),
    RichTextFieldPanel('long_bio'),
]
