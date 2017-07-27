from django.contrib.sitemaps import Sitemap
from django.utils.timezone import datetime, get_default_timezone, make_aware

from core.models import HomePage

from greyjay.articles.models import (
    ArticleListPage,
    ArticlePage,
    ExternalArticleListPage,
    SeriesListPage,
    SeriesPage,
    Topic,
    TopicListPage
)
from greyjay.events.models import EventListPage, EventPage
from greyjay.jobs.models import JobPostingListPage, JobPostingPage
from greyjay.newsletter.models import NewsletterListPage, NewsletterPage
from greyjay.people.models import ContributorListPage, ContributorPage


class HomePageSitemap(Sitemap):
    changefreq = "always"
    priority = 1

    def items(self):
        return HomePage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url


class ArticleListSitemap(Sitemap):
    changefreq = "always"
    priority = 0.6

    def items(self):
        return ArticleListPage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.75

    def items(self):
        return ArticlePage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url


class SeriesListSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return SeriesListPage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url


class SeriesSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.75

    def items(self):
        return SeriesPage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url


class ExternalArticleListSitemap(Sitemap):
    changefreq = "always"
    priority = 0.3

    def items(self):
        return ExternalArticleListPage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url


class TopicSitemap(Sitemap):
    changefreq = "always"
    priority = 0.6

    def items(self):
        return Topic.objects.all()

    def lastmod(self, obj):
        article = obj.articles.first()
        if article:
            return article.latest_revision_created_at
        else:
            return make_aware(datetime.min, get_default_timezone())

    def location(self, obj):
        topic_list_page = TopicListPage.objects.all().first()
        return "{}{}".format(topic_list_page.url, topic_list_page.reverse_subpage('topic', args=(obj.slug, )))


class ContributorListSitemap(Sitemap):
    changefreq = "always"
    priority = 0.6

    def items(self):
        return ContributorListPage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url


class ContributorSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.65

    def items(self):
        return ContributorPage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url


class EventListSitemap(Sitemap):
    changefreq = "always"
    priority = 0.6

    def items(self):
        return EventListPage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url


class EventSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.75

    def items(self):
        return EventPage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url


class JobListSitemap(Sitemap):
    changefreq = "always"
    priority = 0.6

    def items(self):
        return JobPostingListPage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url


class JobSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.75

    def items(self):
        return JobPostingPage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url


class NewsletterListSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.4

    def items(self):
        return NewsletterListPage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url


class NewsletterSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.4

    def items(self):
        return NewsletterPage.objects.live()

    def lastmod(self, obj):
        return obj.latest_revision_created_at

    def location(self, obj):
        return obj.url
