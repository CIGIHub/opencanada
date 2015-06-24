from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, PageChooserPanel,
                                                RichTextFieldPanel)
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.models import register_snippet

from articles import models as article_models
from people import models as people_models


@python_2_unicode_compatible
class HomePage(Page):
    sub_types = [
        article_models.ArticleListPage,
        article_models.InDepthListPage
    ]

    featured_item = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.title

HomePage.content_panels = Page.content_panels + [
    PageChooserPanel("featured_item", "articles.ArticlePage"),
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
