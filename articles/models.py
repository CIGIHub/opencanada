from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                PageChooserPanel,
                                                StreamFieldPanel)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from people import models as people_models

from . import fields as article_fields


@python_2_unicode_compatible
class ArticleListPage(Page):
    subpage_types = ['ArticlePage']

    def __str__(self):
        return self.title


@python_2_unicode_compatible
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
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    # TODO: specify date here or use wagtail page built in date?

    def __str__(self):
        return self.title

ArticlePage.content_panels = Page.content_panels + [
    FieldPanel('subtitle'),
    SnippetChooserPanel('author', people_models.Contributor),
    StreamFieldPanel('body'),
]


@python_2_unicode_compatible
class InDepthListPage(Page):
    subpage_types = ['InDepthPage']

    def __str__(self):
        return self.title


class InDepthArticleLink(Orderable, models.Model):
    override_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="This field is optional. If not provided, the image will be "
                  "pulled from the article page automatically. This field "
                  "allows you to override the automatic image."
    )
    override_text = RichTextField(
        blank=True,
        default="",
        help_text="This field is optional. If not provided, the text will be "
                  "pulled from the article page automatically. This field "
                  "allows you to override the automatic text."
    )
    article = models.ForeignKey(
        "ArticlePage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='series'
    )
    in_depth = ParentalKey(
        "InDepthPage",
        related_name='related_articles'
    )

    panels = [
        PageChooserPanel("article", 'articles.ArticlePage'),
        FieldPanel("override_text"),
        ImageChooserPanel("override_image"),

    ]


class InDepthPage(Page):
    body = article_fields.BodyField(blank=True, default="")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


InDepthPage.content_panels = Page.content_panels + [
    StreamFieldPanel('body'),
    ImageChooserPanel('image'),
    InlinePanel('related_articles', label="Articles")
]
