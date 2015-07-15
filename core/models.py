from __future__ import absolute_import, unicode_literals

from basic_site import models as basic_site_models
from django.db import models
from django.dispatch.dispatcher import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from wagtail.wagtailadmin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.signals import page_published

from articles import models as article_models
from people import models as people_models


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

    featured_item = instance.featured_item.content_type.get_object_for_this_type(id=instance.featured_item.id)

    if hasattr(featured_item, 'feature_style'):
        style = featured_item.feature_style
    else:
        style = "simple"
    if hasattr(featured_item, 'image_overlay_color'):
        color = featured_item.image_overlay_color
    else:
        color = None
    if hasattr(featured_item, 'image_overlay_opacity'):
        opacity = featured_item.image_overlay_opacity
    else:
        opacity = 50
    if hasattr(featured_item, 'font_style'):
        font = featured_item.font_style
    else:
        font = None

    headline = article_models.Headline.objects.filter(containing_page=instance).order_by('-start_date')[:1].first()

    if headline:
        if featured_item != headline.featured_item:
            headline.end_date = now()
            headline.save()
            article_models.Headline.objects.create(
                containing_page=instance,
                featured_item=featured_item,
                feature_style=style,
                image_overlay_color=color,
                image_overlay_opacity=opacity,
                font_style=font
            )
        else:
            headline.feature_style = style
            headline.image_overlay_color = color
            headline.image_overlay_opacity = opacity
            headline.font_style = font

    else:
        if instance.featured_item:
            article_models.Headline.objects.create(
                containing_page=instance,
                featured_item=featured_item,
                feature_style=style,
                image_overlay_color=color,
                image_overlay_opacity=opacity,
                font_style=font
            )


HomePage.content_panels = Page.content_panels + [
    PageChooserPanel("featured_item", "wagtailcore.Page"),
    FieldPanel("number_of_articles"),
]
