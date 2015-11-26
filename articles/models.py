from __future__ import absolute_import, division, unicode_literals

import logging
from itertools import chain
from operator import attrgetter

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.utils.encoding import python_2_unicode_compatible
from modelcluster.fields import ParentalKey
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel, ObjectList,
                                                PageChooserPanel,
                                                StreamFieldPanel,
                                                TabbedInterface)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from core.base import PaginatedListPageMixin, ShareLinksMixin, UniquelySlugable
from people.models import ContributorPage
from themes.models import ThemeablePage

from . import fields as article_fields

logger = logging.getLogger('OpenCanada.ArticleModels')


class ArticleListPage(PaginatedListPageMixin, ThemeablePage):
    subpage_types = ['ArticlePage',
                     ]
    articles_per_page = models.IntegerField(default=20)
    counter_field_name = 'articles_per_page'
    counter_context_name = 'articles'

    filter_choices = [
        ('visualizations', 'Visualizations'),
        ('interviews', 'Interviews'),
        ('editors_pick', "Editor's Pick"),
        ('most_popular', "Most Popular"),
    ]
    filter = models.TextField(choices=filter_choices, null=True, blank=True)

    @property
    def subpages(self):
        if self.filter == "visualizations":
            subpages = ArticlePage.objects.live().filter(visualization=True).order_by('-first_published_at')
        elif self.filter == "interviews":
            subpages = ArticlePage.objects.live().filter(interview=True).order_by('-first_published_at')
        elif self.filter == "editors_pick":
            subpages = ArticlePage.objects.live().filter(editors_pick=True).order_by('-first_published_at')
        elif self.filter == "most_popular":
            subpages = ArticlePage.objects.live().exclude(analytics__isnull=True).order_by('-analytics__last_period_views', '-first_published_at')[:self.articles_per_page]
        else:
            subpages = ArticlePage.objects.live().order_by('-first_published_at')

        return subpages

    content_panels = Page.content_panels + [
        FieldPanel('articles_per_page'),
        FieldPanel('filter', widget=forms.Select),
    ]

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


class ExternalArticleListPage(PaginatedListPageMixin, ThemeablePage):
    subpage_types = ['ExternalArticlePage']

    articles_per_page = models.IntegerField(default=20)
    counter_field_name = 'articles_per_page'
    counter_context_name = 'articles'

    @property
    def subpages(self):
        subpages = ExternalArticlePage.objects.live().descendant_of(self).order_by('-first_published_at')
        return subpages

    content_panels = Page.content_panels + [
        FieldPanel('articles_per_page'),
    ]

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


@python_2_unicode_compatible
class Topic(UniquelySlugable, index.Indexed):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

    @property
    def item_list(self):
        article_list = ArticlePage.objects.live().filter(
            models.Q(primary_topic=self) | models.Q(topic_links__topic=self)
        ).order_by('-first_published_at').distinct()

        series_list = SeriesPage.objects.live().filter(
            primary_topic=self
        ).order_by('-first_published_at').distinct()

        return sorted(chain(article_list, series_list),
                      key=lambda x: x.first_published_at,
                      reverse=True)

    class Meta:
        ordering = ["name", ]

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]
    panels = [
        FieldPanel("name"),
    ]


register_snippet(Topic)


class TopicListPage(RoutablePageMixin, ThemeablePage):
    articles_per_page = models.IntegerField(default=20)

    @property
    def topics(self):
        popular_topics = Topic.objects.annotate(
            num_articles=Count('article_links') + Count('articles') + Count('series')).order_by("-num_articles")[:25]
        return sorted(popular_topics, key=lambda x: x.name)

    @route(r'^$', name="topic_list")
    def topics_list(self, request):
        context = {
            "self": self,
        }
        return render(request, "articles/topic_list_page.html", context)

    @route(r'^([\w-]+)/$', name="topic")
    def topic_view(self, request, topic_slug):
        topic = get_object_or_404(Topic, slug=topic_slug)

        articles = topic.item_list

        paginator = Paginator(articles, self.articles_per_page)
        page = request.GET.get('page')

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context = {
            "self": self,
            "topic": topic,
            "articles": articles,
        }
        return render(request, "articles/topic_page.html", context)

    def get_cached_paths(self):
        yield '/'

        for topic in Topic.objects.all():
            articles = ArticlePage.objects.live().filter(
                models.Q(primary_topic=topic) | models.Q(topic_links__topic=topic)
            ).order_by('-first_published_at').distinct()
            paginator = Paginator(articles, self.articles_per_page)

            topic_url = '/{}/'.format(topic.slug)
            yield topic_url

            for page_number in range(2, paginator.num_pages + 1):
                yield topic_url + '?page=' + str(page_number)

    content_panels = Page.content_panels + [
        FieldPanel('articles_per_page'),
    ]

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


class ArticleCategoryManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


@python_2_unicode_compatible
class ArticleCategory(UniquelySlugable):
    objects = ArticleCategoryManager()

    name = models.CharField(max_length=1024)

    class Meta:
        verbose_name_plural = "Article Categories"
        ordering = ['name', ]

    def natural_key(self):
        return (self.slug,)

    def __str__(self):
        return self.name


register_snippet(ArticleCategory)


class Promotable(models.Model):
    sticky = models.BooleanField(default=False)
    sticky_for_type_section = models.BooleanField(default=False)
    slippery = models.BooleanField(default=False)
    slippery_for_type_section = models.BooleanField(default=False)
    editors_pick = models.BooleanField(default=False)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class FeatureStyle(models.Model):
    name = models.CharField(max_length=100)
    number_of_columns = models.IntegerField(default=1)
    number_of_rows = models.IntegerField(default=1)
    include_image = models.BooleanField(default=False)
    overlay_text = models.BooleanField(default=False)

    def __str__(self):
        return self.name


register_snippet(FeatureStyle)


class FeatureStyleFields(models.Model):
    feature_style = models.ForeignKey(
        FeatureStyle,
        default=2,
        null=True,
        on_delete=models.SET_NULL
    )

    fullbleed_feature = models.BooleanField(default=False)

    image_overlay_opacity = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=45,
        help_text="Set the value from 0 (Solid overlay, original image not visible) to 100 (No overlay, original image completely visible)"
    )

    title_size = models.CharField(
        max_length=20,
        default="medium",
        choices=(
            ('small', 'Smaller'),
            ('medium', 'Medium (default 50px)'),
            ('large', 'Larger')
        )
    )

    def opacity(self):
        return self.image_overlay_opacity / 100

    class Meta:
        abstract = True


class PageLayoutOptions(models.Model):
    include_main_image = models.BooleanField(default=True)
    include_main_image_overlay = models.BooleanField(default=False, help_text="Check to use a full-bleed image layout.",
                                                     verbose_name="Use Main Image Full-Bleed Layout")
    include_caption_in_footer = models.BooleanField(default=False, help_text="Check to display the image caption in the footer.",
                                                    verbose_name="Show caption in footer")
    full_bleed_image_size = models.PositiveSmallIntegerField(default=75,
                                                             help_text="Enter a value from 0 - 100, indicating the percentage of the screen to use for the full-bleed image layout. This value is only used if 'Use Main Image Full-Bleed Layout' is checked.")

    class Meta:
        abstract = True


class ArticlePage(ThemeablePage, FeatureStyleFields, Promotable, ShareLinksMixin, PageLayoutOptions):
    excerpt = RichTextField(blank=True, default="")
    body = article_fields.BodyField()
    chapters = article_fields.ChapterField(blank=True, null=True)
    table_of_contents_heading = models.TextField(blank=True, default="Table of Contents")
    citations_heading = models.TextField(blank=True, default="Works Cited")
    endnotes_heading = models.TextField(blank=True, default="End Notes")
    endnote_identifier_style = models.CharField(
        max_length=20,
        default="roman-lower",
        choices=(
            ('roman-lower', 'Roman Numerals - Lowercase'),
            ('roman-upper', 'Roman Numerals - Uppercase'),
            ('numbers', 'Numbers')
        )
    )

    main_image = models.ForeignKey(
        'images.AttributedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feature_image = models.ForeignKey(
        'images.AttributedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    video_document = models.ForeignKey(
        'wagtaildocs.Document',
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
        related_name='articles'
    )

    category = models.ForeignKey(
        'articles.ArticleCategory',
        related_name='%(class)s',
        on_delete=models.SET_NULL,
        null=True,
        default=1
    )

    include_author_block = models.BooleanField(default=True)

    visualization = models.BooleanField(default=False)
    interview = models.BooleanField(default=False)
    video = models.BooleanField(default=False)
    number_of_related_articles = models.PositiveSmallIntegerField(default=6,
                                                                  verbose_name="Number of Related Articles to Show")

    search_fields = Page.search_fields + (
        index.SearchField('excerpt', partial_match=True),
        index.SearchField('body', partial_match=True),
        index.SearchField('chapters', partial_match=True),
        index.SearchField('get_primary_topic_name', partial_match=True),
        index.SearchField('get_category_name', partial_match=True),
        index.SearchField('get_topic_names', partial_match=True),
        index.SearchField('get_author_names', partial_match=True),
    )

    def __init__(self, *args, **kwargs):
        super(ArticlePage, self).__init__(*args, **kwargs)
        for field in self._meta.fields:
            if field.name == 'first_published_at':
                field.editable = True
                field.blank = True

    def get_primary_topic_name(self):
        if self.primary_topic:
            return self.primary_topic.name
        return ""

    def get_category_name(self):
        if self.category:
            return self.category.name
        return ""

    def get_topic_names(self):
        return '\n'.join([link.topic.name if link.topic else "" for link in self.topic_links.all()])

    def get_author_names(self):
        return '\n'.join(
            [author_link.author.full_name if author_link.author else "" for author_link in self.author_links.all()])

    @property
    def authors(self):
        author_list = []
        for link in self.author_links.all():
            if link.author:
                author_list.append((link.author))
        return author_list

    @property
    def series_articles(self):
        related_series_data = []
        for link in self.series_links.all():
            series_page = link.series
            series_articles = series_page.articles
            series_articles.remove(self)
            related_series_data.append((series_page, series_articles))
        return related_series_data

    @property
    def topics(self):
        primary_topic = self.primary_topic
        all_topics = [link.topic for link in self.topic_links.all()]
        if primary_topic:
            all_topics.append(primary_topic)
        all_topics = list(set(all_topics))
        if len(all_topics) > 0:
            all_topics.sort(key=attrgetter('name'))
        return all_topics

    def related_articles(self, number):
        included = [self.id]
        article_list = []
        if self.primary_topic:
            articles = ArticlePage.objects.live().filter(primary_topic=self.primary_topic).exclude(
                id=self.id).distinct().order_by('-first_published_at')[:number]
            article_list.extend(articles.all())
            included.extend([article.id for article in articles.all()])

        current_total = len(article_list)

        if current_total < number:
            # still don't have enough, so pick using secondary topics
            topics = Topic.objects.filter(article_links__article=self)
            if topics:
                additional_articles = ArticlePage.objects.live().filter(primary_topic__in=topics).exclude(
                    id__in=included).distinct().order_by('-first_published_at')[:number - current_total]
                article_list.extend(additional_articles.all())
                current_total = len(article_list)
                included.extend([article.id for article in additional_articles.all()])

        if current_total < number:
            authors = ContributorPage.objects.live().filter(article_links__article=self)
            if authors:
                additional_articles = ArticlePage.objects.live().filter(author_links__author__in=authors).exclude(
                    id__in=included).distinct().order_by('-first_published_at')[:number - current_total]
                article_list.extend(additional_articles.all())
                current_total = len(article_list)
                included.extend([article.id for article in additional_articles.all()])

        if current_total < number:
            # still don't have enough, so just pick the most recent
            additional_articles = ArticlePage.objects.live().exclude(id__in=included).order_by('-first_published_at')[:number - current_total]
            article_list.extend(additional_articles.all())

        return article_list

    content_panels = Page.content_panels + [
        FieldPanel('excerpt'),
        InlinePanel('author_links', label="Authors"),
        ImageChooserPanel('main_image'),
        ImageChooserPanel('feature_image'),
        DocumentChooserPanel('video_document'),
        StreamFieldPanel('body'),
        SnippetChooserPanel('primary_topic', Topic),
        InlinePanel('topic_links', label="Secondary Topics"),
    ]

    advanced_content_panels = [
        MultiFieldPanel(
            [
                FieldPanel('table_of_contents_heading'),
                StreamFieldPanel('chapters'),
            ],
            heading="Chapters Section"
        ),
        MultiFieldPanel(
            [
                FieldPanel('endnotes_heading'),
                FieldPanel('endnote_identifier_style'),
                InlinePanel('endnote_links', label="End Notes"),
            ],
            heading="End Notes Section"
        ),
        MultiFieldPanel(
            [
                FieldPanel('citations_heading'),
                InlinePanel('citation_links', label="Citations"),
            ],
            heading="Citations Section"
        ),
    ]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel('sticky'),
                FieldPanel('sticky_for_type_section'),
                FieldPanel('slippery'),
                FieldPanel('slippery_for_type_section'),
                FieldPanel('editors_pick'),
                FieldPanel('feature_style'),
                FieldPanel('title_size'),
                FieldPanel('fullbleed_feature'),
                FieldPanel('image_overlay_opacity'),
            ],
            heading="Featuring Settings"
        ),
    ]

    style_panels = ThemeablePage.style_panels + [

        MultiFieldPanel(
            [
                FieldPanel('include_main_image'),
                FieldPanel('include_main_image_overlay'),
                FieldPanel('full_bleed_image_size'),
                FieldPanel('include_caption_in_footer'),
            ],
            heading="Main Image"
        ),
        MultiFieldPanel(
            [
                InlinePanel('background_image_links', label="Background Images"),
            ],
            heading="Background Images"
        ),
        MultiFieldPanel(
            [
                FieldPanel('include_author_block'),
                FieldPanel('number_of_related_articles')
            ],
            heading="Sections"
        ),
        MultiFieldPanel(
            [
                FieldPanel('interview'),
                FieldPanel('video'),
                FieldPanel('visualization'),
            ],
            heading="Categorization"
        )
    ]

    settings_panels = [FieldPanel('first_published_at'), ] + Page.settings_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(advanced_content_panels, heading='Advanced Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(settings_panels, heading='Settings', classname="settings"),
    ])


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
class ExternalArticlePage(Page, FeatureStyleFields, Promotable):
    body = RichTextField()
    website_link = models.URLField(max_length=255)
    main_image = models.ForeignKey(
        'images.AttributedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    source = models.ForeignKey(
        'Source',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return "{}".format(
            self.title
        )

    search_fields = Page.search_fields + (
        index.SearchField('body', partial_match=True),
        index.SearchField('source', partial_match=True),
    )

    def get_source_name(self):
        if self.source:
            return self.source.name
        else:
            return ""

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("website_link"),
        SnippetChooserPanel('source', Source),
        ImageChooserPanel('main_image'),
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
        "people.ContributorPage",
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
        return "{} - {}".format(self.article.title, self.author.full_name)

    panels = [
        PageChooserPanel('author', 'people.ContributorPage'),
    ]


class SeriesListPage(PaginatedListPageMixin, ThemeablePage):
    subpage_types = ['SeriesPage']

    series_per_page = models.IntegerField(default=5)
    counter_field_name = 'series_per_page'
    counter_context_name = 'series_list'

    @property
    def subpages(self):
        subpages = SeriesPage.objects.live().descendant_of(self).order_by('-first_published_at')

        return subpages

    content_panels = Page.content_panels + [
        FieldPanel('series_per_page')
    ]

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


class SeriesArticleLink(Orderable, models.Model):
    override_image = models.ForeignKey(
        'images.AttributedImage',
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
        related_name='series_links'
    )
    series = ParentalKey(
        "SeriesPage",
        related_name='related_article_links'
    )

    panels = [
        PageChooserPanel("article", 'articles.ArticlePage'),
        FieldPanel("override_text"),
        ImageChooserPanel("override_image"),

    ]


class SeriesPage(ThemeablePage, FeatureStyleFields, Promotable, ShareLinksMixin, PageLayoutOptions):
    subtitle = RichTextField(blank=True, default="")
    short_description = RichTextField(blank=True, default="")
    body = article_fields.BodyField(blank=True, default="")

    main_image = models.ForeignKey(
        'images.AttributedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feature_image = models.ForeignKey(
        'images.AttributedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    video_document = models.ForeignKey(
        'wagtaildocs.Document',
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
        related_name='series'
    )

    search_fields = Page.search_fields + (
        index.SearchField('subtitle', partial_match=True),
        index.SearchField('body', partial_match=True),
        index.SearchField('get_primary_topic_name', partial_match=True),
        index.SearchField('get_topic_names', partial_match=True),
    )

    number_of_related_articles = models.PositiveSmallIntegerField(default=6,
                                                                  verbose_name="Number of Related Articles to Show")

    def __init__(self, *args, **kwargs):
        super(SeriesPage, self).__init__(*args, **kwargs)
        for field in self._meta.fields:
            if field.name == 'first_published_at':
                field.editable = True
                field.blank = True

    def get_primary_topic_name(self):
        if self.primary_topic:
            return self.primary_topic.name
        else:
            ""

    def get_topic_names(self):
        return '\n'.join([topic.name if topic else "" for topic in self.topics])

    def get_author_names(self):
        return '\n'.join([author.full_name if author else "" for author in self.authors])

    @property
    def articles(self):
        article_list = []
        for article_link in self.related_article_links.all():
            if article_link.article:
                article_link.article.override_text = article_link.override_text
                article_link.article.override_image = article_link.override_image
                article_list.append(article_link.article)
        return article_list

    @property
    def authors(self):
        author_list = []
        for article_link in self.related_article_links.all():
            if article_link.article:
                if article_link.article:
                    for author_link in article_link.article.author_links.all():
                        if author_link.author:
                            if author_link.author not in author_list:
                                author_list.append(author_link.author)
        author_list.sort(key=attrgetter('last_name'))
        return author_list

    @property
    def topics(self):
        all_topics = []
        if self.primary_topic:
            all_topics.append(self.primary_topic)
        for article_link in self.related_article_links.all():
            if article_link.article:
                all_topics.extend(article_link.article.topics)

        all_topics = list(set(all_topics))
        if all_topics:
            all_topics.sort(key=attrgetter('name'))
        return all_topics

    def related_articles(self, number):
        articles = []
        if self.primary_topic:
            articles = list(ArticlePage.objects.live().filter(primary_topic=self.primary_topic).distinct().order_by(
                '-first_published_at')[:number])

        current_total = len(articles)
        if current_total < number:
            for article in self.articles:
                articles.extend(list(article.related_articles(number)))
                articles = list(set(articles))[:number]
                current_total = len(articles)

                if current_total >= number:
                    return articles

        return articles

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('short_description'),
        ImageChooserPanel('main_image'),
        ImageChooserPanel('feature_image'),
        DocumentChooserPanel('video_document'),
        StreamFieldPanel('body'),
        InlinePanel('related_article_links', label="Articles"),
        SnippetChooserPanel('primary_topic', Topic),
    ]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel('sticky'),
                FieldPanel('sticky_for_type_section'),
                FieldPanel('slippery'),
                FieldPanel('slippery_for_type_section'),
                FieldPanel('editors_pick'),
                FieldPanel('feature_style'),
                FieldPanel('title_size'),
                FieldPanel('fullbleed_feature'),
                FieldPanel('image_overlay_opacity'),
            ],
            heading="Featuring Settings"
        )
    ]

    style_panels = ThemeablePage.style_panels + [
        MultiFieldPanel(
            [
                FieldPanel('include_main_image'),
                FieldPanel('include_main_image_overlay'),
                FieldPanel('full_bleed_image_size'),
                FieldPanel('include_caption_in_footer'),
            ],
            heading="Main Image"
        ),
        MultiFieldPanel(
            [
                FieldPanel('number_of_related_articles'),
            ],
            heading="Sections"
        )
    ]

    settings_panels = [FieldPanel('first_published_at'), ] + Page.settings_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(settings_panels, heading='Settings', classname="settings"),
    ])


@python_2_unicode_compatible
class Headline(FeatureStyleFields):
    containing_page = models.ForeignKey(
        'wagtailcore.Page',
        related_name='historic_headlines'
    )

    featured_item = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return "{}".format(self.id)


@python_2_unicode_compatible
class BackgroundImageBlock(Orderable, UniquelySlugable):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        'images.AttributedImage',
    )
    article = ParentalKey(
        "ArticlePage",
        null=True,
        related_name='background_image_links'
    )

    position = models.CharField(
        max_length=20,
        default="left top",
        choices=(
            ('left top', 'left top'),
            ('left center', 'left center'),
            ('left bottom', "left bottom"),
            ('right top', 'right top'),
            ('right center', 'right center'),
            ('right bottom', "right bottom"),
            ('center top', 'center top'),
            ('center center', 'center center'),
            ('center bottom', "center bottom")
        )
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('image'),
        FieldPanel('position'),
    ]

    def __str__(self):
        return self.name
