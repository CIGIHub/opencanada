from __future__ import absolute_import, unicode_literals

from operator import attrgetter

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
from wagtail.wagtailsnippets.models import register_snippet

from people import models as people_models

from . import fields as article_fields


@python_2_unicode_compatible
class ArticleListPage(Page):
    subpage_types = ['ArticlePage']

    @property
    def subpages(self):
        # Get list of live event pages that are descendants of this page
        subpages = ArticlePage.objects.live().descendant_of(self).order_by('-first_published_at')

        return subpages

    def __str__(self):
        return self.title


class Topic(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

register_snippet(Topic)


@python_2_unicode_compatible
class ArticlePage(Page):
    subtitle = RichTextField(blank=True, default="")
    body = article_fields.BodyField()
    excerpt = RichTextField(blank=True, default="")
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    primary_topic = models.ForeignKey(
        'articles.Topic',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.title

    @property
    def authors(self):
        return [link.author for link in self.author_links.all()]

    @property
    def series_articles(self):
        related_series_data = []
        for link in self.in_depth_links.all():
            indepth_page = link.in_depth
            indepth_articles = indepth_page.articles
            indepth_articles.remove(self)
            related_series_data.append((indepth_page, indepth_articles))
        return related_series_data

    @property
    def topics(self):
        primary_topic = self.primary_topic
        all_topics = [link.topic for link in self.topic_links.all()]
        all_topics.append(primary_topic)
        all_topics = list(set(all_topics))
        all_topics.sort(key=attrgetter('name'))
        return all_topics

    def related_articles(self, number):
        articles = ArticlePage.objects.live().all().exclude(id=self.id)[:number]
        # TODO: pick actual related articles based on primary topic, secondary topics, authors
        return articles

ArticlePage.content_panels = Page.content_panels + [
    FieldPanel('subtitle'),
    InlinePanel('author_links', label="Authors"),
    StreamFieldPanel('body'),
    FieldPanel('excerpt'),
    ImageChooserPanel('main_image'),
    SnippetChooserPanel('primary_topic', Topic),
    InlinePanel('topic_links', label="Secondary Topics"),
]


@python_2_unicode_compatible
class ArticleTopicLink(models.Model):
    topic = models.ForeignKey(
        "Topic",
        related_name='article_links'
    )
    article = ParentalKey(
        "ArticlePage",
        related_name='topic_links'
    )

    def __str__(self):
        return "{} - {}".format(
            self.article.title,
            self.topic.name
        )

    panels = [
        SnippetChooserPanel('topic', Topic),
    ]


@python_2_unicode_compatible
class ArticleAuthorLink(Orderable, models.Model):
    author = models.ForeignKey(
        "people.Contributor",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='article_links'
    )
    article = ParentalKey(
        "ArticlePage",
        related_name='author_links'
    )

    def __str__(self):
        return "{} {} {}".format(self.article.title, self.author.first_name, self.author.last_name)

    panels = [
        SnippetChooserPanel('author', people_models.Contributor),
    ]


@python_2_unicode_compatible
class InDepthListPage(Page):
    subpage_types = ['InDepthPage']

    @property
    def subpages(self):
        # Get list of live event pages that are descendants of this page
        subpages = InDepthPage.objects.live().descendant_of(self).order_by('-first_published_at')

        return subpages

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
        related_name='in_depth_links'
    )
    in_depth = ParentalKey(
        "InDepthPage",
        related_name='related_article_links'
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
    primary_topic = models.ForeignKey(
        'articles.Topic',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def articles(self):
        article_list = []
        for article_link in self.related_article_links.all():
            article_link.article.override_text = article_link.override_text
            article_link.article.override_image = article_link.override_image
            article_list.append(article_link.article)
        return article_list

    @property
    def authors(self):
        author_list = []
        for article_link in self.related_article_links.all():
            for author_link in article_link.article.author_links.all():
                author_list.append(author_link.author)
        author_list.sort(key=attrgetter('last_name'))
        return author_list

    @property
    def topics(self):
        all_topics = [self.primary_topic]
        for article_link in self.related_article_links.all():
            all_topics.extend(article_link.article.topics)

        all_topics = list(set(all_topics))
        all_topics.sort(key=attrgetter('name'))
        return all_topics

InDepthPage.content_panels = Page.content_panels + [
    StreamFieldPanel('body'),
    ImageChooserPanel('image'),
    InlinePanel('related_article_links', label="Articles")
]
