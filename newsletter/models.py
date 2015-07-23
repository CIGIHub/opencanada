from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                PageChooserPanel)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


@python_2_unicode_compatible
class NewsletterPage(Page):
    issue_date = models.DateField("Issue Date", default=now)

    @property
    def articles(self):
        article_list = []
        for article_link in self.article_links.all():
            article_link.article.override_text = article_link.override_text
            article_link.article.override_image = article_link.override_image
            article_list.append(article_link.article)
        return article_list

    def __str__(self):
        return self.issue_date.strftime('%Y-%m-%d')


NewsletterPage.content_panels = Page.content_panels + [
    FieldPanel('issue_date'),
    InlinePanel('article_links', label="Articles"),
    InlinePanel('external_articles', label="External Articles"),
    InlinePanel('events', label="Events"),
]


@python_2_unicode_compatible
class NewsletterArticleLink(Orderable, models.Model):
    article = models.ForeignKey(
        "articles.ArticlePage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='newsletter_links'
    )
    article_text = RichTextField(
        blank=True,
        default="",
        help_text="Text to describe article."
    )
    override_image = models.ForeignKey(
        'images.AttributedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Circular Image to accompany article if article image not selected"
    )
    newsletter = ParentalKey(
        "NewsletterPage",
        related_name='article_links'
    )

    def __str__(self):
        return "{}".format(
            self.article.title
        )

    panels = [
        PageChooserPanel("article", 'articles.ArticlePage'),
        FieldPanel("article_text"),
        ImageChooserPanel("override_image"),

    ]


@python_2_unicode_compatible
class ExternalArticle(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField()
    website_link = models.URLField(max_length=255)
    source = models.ForeignKey(
        'newsletter.Source',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return "{}".format(
            self.title
        )

    content_panels = [
        FieldPanel("title"),
        FieldPanel("body"),
        FieldPanel("website_link")
    ]


@python_2_unicode_compatible
class NewsletterExternalArticleLink(Orderable, ExternalArticle):
    page = ParentalKey(NewsletterPage, related_name='external_articles')

    def __str__(self):
        return "{}".format(
            self.external_article.title
        )


@python_2_unicode_compatible
class Source(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(max_length=255)
    logo = models.ForeignKey(
        'images.AttributedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.name


register_snippet(Source)


Source.panels = [
    FieldPanel('name'),
    FieldPanel('website'),
    ImageChooserPanel('logo'),
]


@python_2_unicode_compatible
class ExternalSourceLink(models.Model):
    source = models.ForeignKey(
        "Source",
        related_name='external_article_links'
    )
    external_article = ParentalKey(
        "ExternalArticle",
        related_name='source_link'
    )

    def __str__(self):
        return "{} - {}".format(
            self.external_article.title,
            self.source.name
        )

    panels = [
        SnippetChooserPanel('source', Source),
    ]


@python_2_unicode_compatible
class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField("Issue Date")
    location = models.CharField(max_length=255)
    event_link = models.URLField(max_length=255)
    organization = models.ForeignKey(
        'newsletter.Organization',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return "{}".format(
            self.title
        )

    content_panels = [
        FieldPanel("title"),
        FieldPanel("date"),
        FieldPanel("location"),
        FieldPanel("event_link")
    ]


@python_2_unicode_compatible
class NewsletterEventLink(Orderable, Event):
    page = ParentalKey(NewsletterPage, related_name='event')

    def __str__(self):
        return "{}".format(
            self.event.title
        )


@python_2_unicode_compatible
class Organization(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(max_length=255)
    logo = models.ForeignKey(
        'images.AttributedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.name


register_snippet(Organization)


Organization.panels = [
    FieldPanel('name'),
    FieldPanel('website'),
    ImageChooserPanel('logo'),
]


@python_2_unicode_compatible
class EventOrganizationLink(models.Model):
    organization = models.ForeignKey(
        "Organization",
        related_name='event_links'
    )
    events = ParentalKey(
        "Event",
        related_name='organization_link'
    )

    def __str__(self):
        return "{} - {}".format(
            self.event.title,
            self.organization.name
        )

    panels = [
        SnippetChooserPanel('organization', Organization),
    ]
