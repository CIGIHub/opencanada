from __future__ import absolute_import, unicode_literals

from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel, RichTextFieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from basic_site.models import BasePage
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
