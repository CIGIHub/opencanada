from __future__ import absolute_import, unicode_literals

import itertools

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch.dispatcher import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                                ObjectList, PageChooserPanel,
                                                StreamFieldPanel,
                                                TabbedInterface)
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.signals import page_published
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

from greyjay.articles import fields as article_fields
from greyjay.articles import models as article_models
from greyjay.events import models as event_models
from greyjay.jobs import models as jobs_models
from greyjay.newsletter import models as newsletter_models
from greyjay.people import models as people_models
from greyjay.projects import models as project_models
from greyjay.themes.models import ThemeablePage


class StreamPage(ThemeablePage):
    body = article_fields.BodyField()

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


@python_2_unicode_compatible
class HomePage(ThemeablePage):
    subpage_types = [
        article_models.ArticleListPage,
        article_models.SeriesListPage,
        article_models.TopicListPage,
        people_models.ContributorListPage,
        project_models.ProjectListPage,
        newsletter_models.NewsletterListPage,
        event_models.EventListPage,
        article_models.ExternalArticleListPage,
        jobs_models.JobPostingListPage,
        StreamPage,
    ]

    featured_item = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    number_of_rows_of_articles = models.IntegerField(default=12, verbose_name="Rows")
    number_of_columns_of_articles = models.IntegerField(default=3, verbose_name="Columns")
    number_of_rows_of_series = models.IntegerField(default=1, verbose_name="Rows")
    number_of_rows_of_external_articles = models.IntegerField(default=2, verbose_name="Rows")
    number_of_columns_of_external_articles = models.IntegerField(default=2, verbose_name="Columns")
    number_of_rows_of_visualizations = models.IntegerField(default=2, verbose_name="Rows")
    number_of_columns_of_visualizations = models.IntegerField(default=2, verbose_name="Columns")
    full_bleed_image_size = models.PositiveSmallIntegerField(default=90, help_text="Enter a value from 0 - 100, indicating the percentage of the screen to use for the featured image layout.")

    _articles = None
    _most_popular_article = None

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
        if self._articles is not None:
            return self._articles

        article_content_type = ContentType.objects.get_for_model(
            article_models.ArticlePage)
        series_content_type = ContentType.objects.get_for_model(
            article_models.SeriesPage)

        articles = Page.objects.live().filter(
            models.Q(content_type=article_content_type)
            | models.Q(content_type=series_content_type)
        ).annotate(
            sticky=models.Case(
                models.When(
                    models.Q(seriespage__sticky=True) | (models.Q(articlepage__sticky=True)),
                    then=models.Value(1)),
                default=models.Value(0),
                output_field=models.IntegerField())
        ).exclude(
            models.Q(seriespage__slippery=True) | models.Q(articlepage__slippery=True)
        ).order_by("-sticky", "-first_published_at")

        used = []
        if self.featured_item:
            used.append(self.featured_item.id)
        self._articles = self.get_article_set(self.number_of_columns_of_articles,
                                              self.number_of_rows_of_articles, articles,
                                              used)

        return self._articles

    @property
    def most_popular_article(self):
        if self._most_popular_article is not None:
            return self._most_popular_article

        def get_views(article):
            try:
                if article.analytics:
                    return article.analytics.last_period_views
            except:
                return 0

        # flatten the list of lists with generator
        articles = itertools.chain.from_iterable(self.articles)
        articles_by_popularity = sorted(
            articles,
            key=get_views
        )

        self._most_popular_article = articles_by_popularity[-1]
        return self._most_popular_article

    @property
    def typed_featured_item(self):
        if self.featured_item:
            featured_item = self.featured_item.content_type.get_object_for_this_type(
                id=self.featured_item.id)
            return featured_item

    def get_rows(self, number_of_rows, number_of_columns, items):
        rows = []

        for row_index in range(0, number_of_rows):
            row = items[(row_index * number_of_columns):(row_index * number_of_columns) + number_of_columns]
            rows.append(row)

        return rows

    @property
    def external_articles(self):
        number_of_external_articles = self.number_of_rows_of_external_articles * self.number_of_columns_of_external_articles
        external_article_list = article_models.ExternalArticlePage.objects.live().order_by("-first_published_at")[:number_of_external_articles]

        return self.get_rows(self.number_of_rows_of_external_articles,
                             self.number_of_columns_of_external_articles,
                             external_article_list)

    @property
    def graphics(self):
        number_of_graphics = self.number_of_rows_of_visualizations * self.number_of_columns_of_visualizations
        graphics_list = article_models.ArticlePage.objects.live().filter(
            visualization=True).annotate(
            sticky_value=models.Case(
                models.When(models.Q(sticky_for_type_section=True),
                            then=models.Value(1)), default=models.Value(0),
                output_field=models.IntegerField())
        ).exclude(
            slippery_for_type_section=True
        ).order_by("-sticky_value", "-first_published_at")[:number_of_graphics]

        return self.get_rows(self.number_of_rows_of_visualizations, self.number_of_columns_of_visualizations, graphics_list)

    @property
    def series(self):
        number_of_series = self.number_of_rows_of_series
        series_list = article_models.SeriesPage.objects.live().annotate(
            sticky_value=models.Case(
                models.When(models.Q(sticky_for_type_section=True), then=models.Value(1)), default=models.Value(0),
                output_field=models.IntegerField())
        ).exclude(
            slippery_for_type_section=True
        ).order_by("-sticky_value", "-first_published_at")[:number_of_series]

        return self.get_rows(self.number_of_rows_of_series, 1, series_list)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                PageChooserPanel("featured_item", "wagtailcore.Page"),
                FieldPanel("full_bleed_image_size"),
            ],
            heading="Main Feature"
        ),
        MultiFieldPanel(
            [
                FieldPanel("number_of_rows_of_articles"),
                FieldPanel("number_of_columns_of_articles"),
            ],
            heading="Main Feed Settings"
        ),
        MultiFieldPanel(
            [
                FieldPanel("number_of_rows_of_series"),
            ],
            heading="Series Section Settings"
        ),
        MultiFieldPanel(
            [
                FieldPanel("number_of_rows_of_external_articles"),
                FieldPanel("number_of_columns_of_external_articles"),
            ],
            heading="External Articles Section Settings"
        ),
        MultiFieldPanel(
            [
                FieldPanel("number_of_rows_of_visualizations"),
                FieldPanel("number_of_columns_of_visualizations"),
            ],
            heading="Visualization Section Settings"
        ),
    ]

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


@receiver(page_published, sender=HomePage)
def on_publish(**kwargs):
    instance = kwargs["instance"]

    featured_item = instance.featured_item.content_type.get_object_for_this_type(
        id=instance.featured_item.id)

    if hasattr(featured_item, 'feature_style'):
        style = featured_item.feature_style
    else:
        style = "simple"
    if hasattr(featured_item, 'image_overlay_opacity'):
        opacity = featured_item.image_overlay_opacity
    else:
        opacity = 50

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
                image_overlay_opacity=opacity,
            )
        else:
            headline.feature_style = style
            headline.image_overlay_opacity = opacity

    else:
        if instance.featured_item:
            article_models.Headline.objects.create(
                containing_page=instance,
                featured_item=featured_item,
                feature_style=style,
                image_overlay_opacity=opacity,
            )


@python_2_unicode_compatible
class SiteDefaults(models.Model):
    site = models.OneToOneField('wagtailcore.Site',
                                related_name='default_settings', unique=True)
    default_external_article_source_logo = models.ForeignKey(
        'images.AttributedImage',
        related_name='+'
    )
    contact_email = models.EmailField(blank=True, default="")

    def __str__(self):
        return "{}".format(self.site)

    class Meta:
        verbose_name_plural = "Site Defaults"

    panels = [
        FieldPanel('site'),
        ImageChooserPanel('default_external_article_source_logo'),
        FieldPanel('contact_email'),
    ]
register_snippet(SiteDefaults)
