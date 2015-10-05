from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                ObjectList, PageChooserPanel,
                                                TabbedInterface)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from themes.models import ThemeablePage


@python_2_unicode_compatible
class NewsletterListPage(ThemeablePage):
    subpage_types = ['NewsletterPage']
    intro_text = RichTextField()
    body = RichTextField()

    @property
    def subpages(self):
        subpages = NewsletterPage.objects.live().descendant_of(self).order_by('-issue_date')

        return subpages

    def __str__(self):
        return self.title

    content_panels = Page.content_panels + [
        FieldPanel('intro_text'),
        FieldPanel('body'),
    ]

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


@python_2_unicode_compatible
class NewsletterPage(ThemeablePage):
    issue_date = models.DateField("Issue Date", default=now)

    @property
    def articles(self):
        article_list = []
        for article_link in self.article_links.all():
            article_link.article.override_text = article_link.override_text
            article_link.article.override_image = article_link.override_image
            article_list.append(article_link.article)
        return article_list

    @property
    def external_articles(self):
        external_article_list = []
        for article_link in self.external_article_links.all():
            article_link.external_article.override_text = article_link.override_text
            external_article_list.append(article_link.external_article)
        return external_article_list

    @property
    def events(self):
        event_list = []
        for event_link in self.event_links.all():
            event_link.event.override_text = event_link.override_text
            event_list.append(event_link.event)
        return event_list

    def __str__(self):
        return self.issue_date.strftime('%Y-%m-%d')

    content_panels = Page.content_panels + [
        FieldPanel('issue_date'),
        InlinePanel('article_links', label="Articles", help_text='The first article will be the newsletter feature story'),
        InlinePanel('external_article_links', label="External Articles"),
        InlinePanel('event_links', label="Events"),
    ]

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


@python_2_unicode_compatible
class NewsletterArticleLink(Orderable, models.Model):
    article = models.ForeignKey(
        "articles.ArticlePage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='newsletter_links',
        help_text="Link to an internal article"
    )
    override_text = RichTextField(
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
        FieldPanel("override_text"),
        ImageChooserPanel("override_image"),
    ]


@python_2_unicode_compatible
class NewsletterExternalArticleLink(Orderable, models.Model):
    external_article = models.ForeignKey(
        "articles.ExternalArticlePage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='newsletter_links',
        help_text="Link to an external article"
    )
    override_text = RichTextField(
        blank=True,
        default="",
        help_text="Text to describe article."
    )

    newsletter = ParentalKey(
        "NewsletterPage",
        related_name='external_article_links'
    )

    def __str__(self):
        return "{}".format(
            self.external_article.title
        )

    panels = [
        PageChooserPanel("external_article", 'articles.ExternalArticlePage'),
        FieldPanel("override_text"),
    ]


@python_2_unicode_compatible
class NewsletterEventLink(Orderable, models.Model):
    event = models.ForeignKey(
        "events.EventPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='newsletter_links',
        help_text="Link to an event"
    )
    override_text = RichTextField(
        blank=True,
        default="",
        help_text="Text to describe this event."
    )

    newsletter = ParentalKey(
        "NewsletterPage",
        related_name='event_links'
    )

    def __str__(self):
        return "{}".format(
            self.event.title
        )

    panels = [
        PageChooserPanel("event", 'events.EventPage'),
        FieldPanel("override_text"),
    ]
