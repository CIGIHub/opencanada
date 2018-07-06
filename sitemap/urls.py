from django.urls import re_path
from django.contrib.sitemaps.views import sitemap

from . import models

sitemaps = {
    "Home": models.HomePageSitemap,
    "Articles": models.ArticleSitemap,
    "ArticleLists": models.ArticleListSitemap,
    "Series": models.SeriesSitemap,
    "SeriesLists": models.SeriesListSitemap,
    "ExternalArticles": models.ExternalArticleListSitemap,
    "Topics": models.TopicSitemap,
    "Contributors": models.ContributorSitemap,
    "ContributorLists": models.ContributorListSitemap,
    "Events": models.EventSitemap,
    "EventsLists": models.EventListSitemap,
    "Jobs": models.JobSitemap,
    "JobsLists": models.JobListSitemap,
    "Newsletters": models.NewsletterSitemap,
    "NewsletterLists": models.NewsletterListSitemap,
}

urlpatterns = [
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]
