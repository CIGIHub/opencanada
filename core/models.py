from __future__ import absolute_import, unicode_literals

from basic_site import models as basic_site_models
from django.db import models
from django.dispatch.dispatcher import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from wagtail.wagtailadmin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.signals import page_published
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from articles import models as article_models
from people import models as people_models


@python_2_unicode_compatible
class FontStyle(models.Model):
    name = models.CharField(max_length=1024)
    font_size = models.FloatField(default=1, help_text="The size of the fonts in ems.")
    line_size = models.FloatField(default=100, help_text="The line height as a percentage.")
    text_colour = models.CharField(max_length=64, default="#000000", help_text="The colour of the text in hexidecimal. For example, to get black enter '#000000'.")

    panels = [
        FieldPanel('name'),
        FieldPanel('font_size'),
        FieldPanel('line_size'),
        FieldPanel('text_colour'),
    ]

    def __str__(self):
        return self.name


register_snippet(FontStyle)


@python_2_unicode_compatible
class HomePage(Page):
    subpage_types = [
        article_models.ArticleListPage,
        article_models.InDepthListPage,
        article_models.TopicListPage,
        people_models.ContributorListPage,
        basic_site_models.BasicStreamPage,
    ]

    featured_item = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    featured_item_font_style = models.ForeignKey(
        'core.FontStyle',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    number_of_articles = models.IntegerField(default=12)

    def __str__(self):
        return self.title

    @property
    def articles(self):
        articles = article_models.ArticlePage.objects.live().all().order_by("-first_published_at")[:self.number_of_articles]
        return articles


@receiver(page_published, sender=HomePage)
def on_publish(**kwargs):
    instance = kwargs["instance"]

    headline = article_models.Headline.objects.filter(containing_page=instance).order_by('-start_date')[:1].first()
    if headline:
        if instance.featured_item != headline.featured_item:
            headline.end_date = now()
            headline.save()
            article_models.Headline.objects.create(
                containing_page=instance,
                featured_item=instance.featured_item,
                featured_item_font_style=instance.featured_item_font_style
            )
        else:
            headline.featured_item_font_style = instance.featured_item_font_style
    else:
        if instance.featured_item:
            article_models.Headline.objects.create(
                containing_page=instance,
                featured_item=instance.featured_item,
                featured_item_font_style=instance.featured_item_font_style
            )


HomePage.content_panels = Page.content_panels + [
    PageChooserPanel("featured_item", "articles.ArticlePage"),
    SnippetChooserPanel("featured_item_font_style", FontStyle),
    FieldPanel("number_of_articles"),
]
