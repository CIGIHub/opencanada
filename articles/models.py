from __future__ import absolute_import, unicode_literals

from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from people import models as people_models

from . import fields as article_fields


class ArticleListPage(Page):
    pass


class ArticlePage(Page):
    subtitle = RichTextField(blank=True, default="")
    author = models.ForeignKey(
        "people.Contributor",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = article_fields.BodyField()
    excerpt = RichTextField(blank=True, default="")


ArticlePage.content_panels = Page.content_panels + [
    FieldPanel('subtitle'),
    SnippetChooserPanel('author', people_models.Contributor),
    StreamFieldPanel('body'),
]
#
# class InDepthArticleLink(models.Model):
#     image = models.ForeignKey(
#         'wagtailimages.Image',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='+'
#     )
#     text = RichTextField()
#     article = models.ForeignKey(
#         "ArticlePage",
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='+'
#     )
#     in_depth = ParentalKey(
#         "InDepthPage",
#         related_name='related_articles'
#     )
#
#     panels = [
#         FieldPanel("text"),
#         ImageChooserPanel("image"),
#         PageChooserPanel("article", 'core.ArticlePage')
#     ]
#
#
# class InDepthPage(Page):
#     intro = RichTextField(blank=True, default="")
#     image = models.ForeignKey(
#         'wagtailimages.Image',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='+'
#     )
#
#
# InDepthPage.content_panels = [
#     RichTextFieldPanel('intro'),
#     ImageChooserPanel('image'),
#     InlinePanel('related_articles')
# ]
