from __future__ import absolute_import, division, unicode_literals

from datetime import timedelta
from operator import attrgetter

import requests
from basic_site.models import UniquelySlugable
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from modelcluster.fields import ParentalKey
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel, ObjectList,
                                                PageChooserPanel,
                                                StreamFieldPanel,
                                                TabbedInterface)
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from people.models import ContributorPage

from . import fields as article_fields


@python_2_unicode_compatible
class Colour(models.Model):
    name = models.CharField(max_length=100)
    hex_value = models.CharField(max_length=7)

    def rgb(self):
        split = (self.hex_value[1:3], self.hex_value[3:5], self.hex_value[5:7])
        rgb_value = [str(int(x, 16)) for x in split]
        rgb_string = ', '.join(rgb_value)
        return rgb_string

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.hex_value.startswith("#"):
            self.hex_value = "#{}".format(self.hex_value)
        super(Colour, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name', ]

register_snippet(Colour)


@python_2_unicode_compatible
class FontStyle(models.Model):
    name = models.CharField(max_length=1024)
    font_size = models.FloatField(default=1, help_text="The size of the fonts in ems.")
    line_size = models.FloatField(default=100, help_text="The line height as a percentage.")
    text_colour = models.ForeignKey(
        Colour,
        default=1,
        null=True,
        on_delete=models.SET_NULL
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('font_size'),
        FieldPanel('line_size'),
        FieldPanel('text_colour'),
    ]

    def __str__(self):
        return self.name


register_snippet(FontStyle)


class ArticleListPage(Page):
    subpage_types = ['ArticlePage',
                     'ChapteredArticlePage',
                     ]

    articles_per_page = models.IntegerField(default=20)

    @property
    def subpages(self):
        # Get list of live event pages that are descendants of this page
        subpages = ArticlePage.objects.live().descendant_of(self).order_by('-first_published_at')

        return subpages

    def get_context(self, request):
        articles = self.subpages

        page = request.GET.get('page')
        paginator = Paginator(articles, self.articles_per_page)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context = super(ArticleListPage, self).get_context(request)
        context['articles'] = articles
        return context

    content_panels = Page.content_panels + [
        FieldPanel('articles_per_page')
    ]


class ExternalArticleListPage(Page):
    subpage_types = ['ExternalArticlePage']

    articles_per_page = models.IntegerField(default=20)

    @property
    def subpages(self):
        subpages = ExternalArticlePage.objects.live().descendant_of(self).order_by('-first_published_at')

        return subpages

    def get_context(self, request):
        articles = self.subpages

        page = request.GET.get('page')
        paginator = Paginator(articles, self.articles_per_page)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context = super(ExternalArticleListPage, self).get_context(request)
        context['articles'] = articles
        return context

    content_panels = Page.content_panels + [
        FieldPanel('articles_per_page')
    ]


@python_2_unicode_compatible
class Topic(UniquelySlugable):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", ]

register_snippet(Topic)


Topic.panels = [
    FieldPanel("name"),
]


class TopicListPage(RoutablePageMixin, Page):

    @property
    def topics(self):
        popular_topics = Topic.objects.annotate(num_articles=Count('article_links') + Count('articles') + Count('series')).order_by("-num_articles")[:25]
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

        articles = ArticlePage.objects.live().filter(
            models.Q(primary_topic=topic) | models.Q(topic_links__topic=topic)
        ).order_by('-first_published_at').distinct()

        context = {
            "self": self,
            "topic": topic,
            "articles": articles,
        }
        return render(request, "articles/topic_page.html", context)


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
        return (self.slug, )

    def __str__(self):
        return self.name


register_snippet(ArticleCategory)


class Promotable(models.Model):
    sticky = models.BooleanField(default=False)
    editors_pick = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Sharelinks(models.Model):
    cached_twitter_count = models.IntegerField(default=0)
    cached_facebook_count = models.IntegerField(default=0)
    cached_last_updated = models.DateTimeField(blank=True, null=True)

    def update_cache(self):
        if not self.cached_last_updated or (timezone.now() - self.cached_last_updated) > timedelta(minutes=10):
            url = 'https://cdn.api.twitter.com/1/urls/count.json?url=http://opencanada.org' + self.url
            response = requests.get(url)
            j = response.json()
            self.cached_twitter_count = j['count']

            url = 'https://graph.facebook.com/?id=http://opencanada.org' + self.url
            response = requests.get(url)
            j = response.json()
            self.cached_facebook_count = j['shares']

            self.cached_last_updated = timezone.now()
            self.save()

    @property
    def twitter_count(self):
        self.update_cache()
        return self.cached_twitter_count

    @property
    def facebook_count(self):
        self.update_cache()
        return self.cached_facebook_count

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

    image_overlay_color = models.ForeignKey(
        Colour,
        default=1,
        null=True,
        on_delete=models.SET_NULL
    )

    image_overlay_opacity = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=30,
        help_text="Set the value from 0 (Solid overlay, original image not visible) to 100 (No overlay, original image completely visible)"
    )

    font_style = models.ForeignKey(
        'articles.FontStyle',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def opacity(self):
        return self.image_overlay_opacity / 100

    class Meta:
        abstract = True


class ArticlePage(Page, FeatureStyleFields, Promotable, Sharelinks):
    excerpt = RichTextField(blank=True, default="")
    body = article_fields.BodyField()

    main_image = models.ForeignKey(
        'images.AttributedImage',
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
        null=True
    )

    include_author_block = models.BooleanField(default=True)
    include_main_image = models.BooleanField(default=True)

    search_fields = Page.search_fields + (
        index.SearchField('excerpt', partial_match=True),
        index.SearchField('body', partial_match=True),
        index.SearchField('get_primary_topic_name', partial_match=True),
        index.SearchField('get_category_name', partial_match=True),
        index.SearchField('get_topic_names', partial_match=True),
        index.SearchField('get_author_names', partial_match=True),
    )

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
        return '\n'.join([author_link.author.full_name if author_link.author else "" for author_link in self.author_links.all()])

    @property
    def authors(self):
        return [link.author for link in self.author_links.all()]

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
        articles = ArticlePage.objects.live().filter(primary_topic=self.primary_topic).exclude(id=self.id).distinct().order_by('-first_published_at')[:number]
        article_list = list(articles.all())
        included.extend([article.id for article in articles.all()])

        current_total = len(article_list)
        if current_total < number:
            # still don't have enough, so pick using secondary topics
            topics = Topic.objects.filter(article_links__article=self)
            additional_articles = ArticlePage.objects.live().filter(primary_topic__in=topics).exclude(id__in=included).distinct().order_by('-first_published_at')[:number - current_total]
            article_list.extend(additional_articles.all())
            current_total = len(article_list)
            included.extend([article.id for article in additional_articles.all()])

        if current_total < number:
            authors = ContributorPage.objects.live().filter(article_links__article=self)
            additional_articles = ArticlePage.objects.live().filter(author_links__author__in=authors).exclude(id__in=included).distinct().order_by('-first_published_at')[:number - current_total]
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
        StreamFieldPanel('body'),
        SnippetChooserPanel('primary_topic', Topic),
        InlinePanel('topic_links', label="Secondary Topics"),
        SnippetChooserPanel('category', ArticleCategory),
    ]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel('sticky'),
                FieldPanel('editors_pick'),
                FieldPanel('feature_style'),
                MultiFieldPanel(
                    [
                        FieldPanel('image_overlay_opacity'),
                        SnippetChooserPanel('image_overlay_color', Colour),
                        SnippetChooserPanel("font_style", FontStyle),
                    ],
                    heading="Image Overlay Settings"
                )
            ],
            heading="Featuring Settings"
        ),
    ]

    style_panels = [
        MultiFieldPanel(
            [
                FieldPanel('include_main_image'),
                FieldPanel('include_author_block'),
            ],
            heading="Sections"
        )
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


class ChapteredArticlePage(ArticlePage):
    chapters = article_fields.ChapterField(blank=True, null=True)
    works_cited = StreamField(
        block_types=[
            ('citation', article_fields.CitationBlock()),
        ],
        blank=True, null=True
    )

    end_notes = StreamField(
        block_types=[
            ('end_note', article_fields.EndNoteBlock()),
        ],
        blank=True, null=True
    )


ChapteredArticlePage.content_panels = Page.content_panels + [
    FieldPanel('excerpt'),
    InlinePanel('author_links', label="Authors"),
    ImageChooserPanel('main_image'),
    StreamFieldPanel('body'),
    SnippetChooserPanel('primary_topic', Topic),
    InlinePanel('topic_links', label="Secondary Topics"),
    SnippetChooserPanel('category', ArticleCategory),
    StreamFieldPanel('chapters'),
    StreamFieldPanel('works_cited'),
    StreamFieldPanel('end_notes'),
    # InlinePanel('chapters', label="Chapters"),
]

#
# class Chapter(models.Model):
#     heading = models.CharField(max_length=512, blank=True)
#     body = article_fields.BodyField(blank=True, null=True)
#
#     content_panels = [
#         FieldPanel('heading'),
#         StreamFieldPanel('body'),
#     ]
#
#     class Meta:
#         abstract = True
#
#
# class ArticleChapter(Orderable, Chapter):
#     page = ParentalKey(ChapteredArticlePage, related_name='chapters')


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


class SeriesListPage(Page):
    subpage_types = ['SeriesPage']

    series_per_page = models.IntegerField(default=5)

    @property
    def subpages(self):
        subpages = SeriesPage.objects.live().descendant_of(self).order_by('-first_published_at')

        return subpages

    def get_context(self, request):
        series_list = self.subpages

        page = request.GET.get('page')
        paginator = Paginator(series_list, self.series_per_page)
        try:
            series_list = paginator.page(page)
        except PageNotAnInteger:
            series_list = paginator.page(1)
        except EmptyPage:
            series_list = paginator.page(paginator.num_pages)

        context = super(SeriesListPage, self).get_context(request)
        context['series_list'] = series_list
        return context

    content_panels = Page.content_panels + [
        FieldPanel('series_per_page')
    ]


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


class SeriesPage(Page, FeatureStyleFields, Promotable, Sharelinks):
    subtitle = RichTextField(blank=True, default="")
    body = article_fields.BodyField(blank=True, default="")

    main_image = models.ForeignKey(
        'images.AttributedImage',
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

    def get_primary_topic_name(self):
        return self.primary_topic.name

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
        articles = list(ArticlePage.objects.live().filter(primary_topic=self.primary_topic).distinct().order_by('-first_published_at')[:number])

        current_total = len(articles)

        for article in self.articles:
            if current_total < number:
                articles.extend(list(article.related_articles(number)))
                articles = list(set(articles))[:number]
                current_total = len(articles)
            else:
                return articles

        return articles

SeriesPage.content_panels = Page.content_panels + [
    FieldPanel('subtitle'),
    ImageChooserPanel('main_image'),
    StreamFieldPanel('body'),
    InlinePanel('related_article_links', label="Articles"),
]

SeriesPage.promote_panels = Page.promote_panels + [
    MultiFieldPanel(
        [
            FieldPanel('sticky'),
            FieldPanel('editors_pick'),
            FieldPanel('feature_style'),
            MultiFieldPanel(
                [
                    FieldPanel('image_overlay_opacity'),
                    SnippetChooserPanel('image_overlay_color', Colour),
                    SnippetChooserPanel("font_style", FontStyle),
                ],
                heading="Image Overlay Settings"
            )
        ],
        heading="Featuring Settings"
    )
]


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
