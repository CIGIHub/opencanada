from __future__ import absolute_import, unicode_literals

from basic_site import models as basic_site_models
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch.dispatcher import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from wagtail.wagtailadmin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.signals import page_published

from articles import models as article_models
from events import models as event_models
from newsletter import models as newsletter_models
from people import models as people_models


@python_2_unicode_compatible
class HomePage(Page):
    subpage_types = [
        article_models.ArticleListPage,
        article_models.SeriesListPage,
        article_models.TopicListPage,
        people_models.ContributorListPage,
        basic_site_models.BasicStreamPage,
        newsletter_models.NewsletterListPage,
        event_models.EventListPage,
        article_models.ExternalArticleListPage,
    ]

    featured_item = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    number_of_rows_of_articles = models.IntegerField(default=12)
    number_of_columns_of_articles = models.IntegerField(default=3)

    def __str__(self):
        return self.title

    def get_article_set(self, columns, rows, article_list, used):
        if columns == 0 and rows == 0 or not article_list:
            return []

        current_set = []
        while rows > 0:
            row, height = self._fill_row(columns, article_list, used, rows)
            current_set.append(row)
            rows = rows - height

        return current_set

    def _fill_row(self, columns, article_list, used, max_height):
        if columns == 0 or not article_list:
            return [], 0

        for article in article_list.all():
            typed_article = article.content_type.get_object_for_this_type(
                id=article.id)
            if typed_article.feature_style.number_of_columns <= columns \
                    and typed_article.id not in used\
                    and typed_article.feature_style.number_of_rows <= max_height:

                columns = columns - typed_article.feature_style.number_of_columns
                used.append(typed_article.id)
                row = [typed_article]
                max_height = min(max_height, typed_article.feature_style.number_of_rows)

                if max_height > 1 and columns > 0:
                    subset = self.get_article_set(columns, max_height, article_list, used)
                    row.append(subset)
                else:
                    recursive_row, height = self._fill_row(columns, article_list, used, max_height)
                    row.extend(recursive_row)
                return row, max_height

        return [], 0

    @property
    def articles(self):
        article_content_type = ContentType.objects.get_for_model(
            article_models.ArticlePage)
        series_content_type = ContentType.objects.get_for_model(
            article_models.SeriesPage)

        articles = Page.objects.live().filter(
            models.Q(content_type=article_content_type) | models.Q(content_type=series_content_type)
        ).annotate(
            sticky=models.Case(
                models.When(
                    models.Q(seriespage__sticky=True) | (models.Q(articlepage__sticky=True)),
                    then=models.Value(1)),
                default=models.Value(0),
                output_field=models.IntegerField())).order_by("-sticky", "-first_published_at")

        return self.get_article_set(self.number_of_columns_of_articles,
                                    self.number_of_rows_of_articles, articles,
                                    [])

    @property
    def typed_featured_item(self):
        if self.featured_item:
            featured_item = self.featured_item.content_type.get_object_for_this_type(
                id=self.featured_item.id)
            return featured_item

    @property
    def external_articles(self):
        external_article_list = article_models.ExternalArticlePage.objects.live().order_by("-first_published_at")[:4]
        external_article_list = [external_article_list[:2], external_article_list[2:4]]

        return external_article_list


@receiver(page_published, sender=HomePage)
def on_publish(**kwargs):
    instance = kwargs["instance"]

    featured_item = instance.featured_item.content_type.get_object_for_this_type(
        id=instance.featured_item.id)

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

    headline = article_models.Headline.objects.filter(
        containing_page=instance).order_by('-start_date')[:1].first()

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
    FieldPanel("number_of_rows_of_articles"),
    FieldPanel("number_of_columns_of_articles"),
]
