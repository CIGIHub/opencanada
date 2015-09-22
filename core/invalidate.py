
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from wagtail.contrib.wagtailfrontendcache.utils import purge_page_from_cache
from wagtail.wagtailcore.signals import page_published

from articles import models as articles_models
from core.models import HomePage
from events.models import EventListPage, EventPage
from jobs.models import JobPostingListPage, JobPostingPage
from newsletter.models import NewsletterListPage, NewsletterPage
from people.models import ContributorListPage, ContributorPage

# for cache invalidation of index pages
invalidation_map = {
    JobPostingPage: [JobPostingListPage],

    EventPage: [EventListPage],

    ContributorPage: [ContributorListPage],

    NewsletterPage: [NewsletterListPage],

    articles_models.ArticlePage: [
        articles_models.ArticleListPage,
        articles_models.TopicListPage,
        articles_models.SeriesListPage,
        HomePage
    ],

    articles_models.ChapteredArticlePage: [
        articles_models.ArticleListPage,
        articles_models.TopicListPage,
        articles_models.SeriesListPage,
        HomePage,
    ],

    articles_models.SeriesPage: [
        articles_models.ArticleListPage,
        articles_models.TopicListPage,
        articles_models.SeriesListPage,
        HomePage,
    ],

    articles_models.ExternalArticlePage: [
        articles_models.ArticleListPage,
        HomePage,
    ]
}


# TODO: Invalidate related pages when possible.


def purge_related(instance):
    global invalidation_map
    instance_model = instance.__class__
    if instance_model not in invalidation_map:
        return
    for related_page_model in invalidation_map[instance_model]:
        for page in related_page_model.objects.live():
            purge_page_from_cache(page)


@receiver(page_published)
def blog_published_handler(instance, **kwargs):
    purge_related(instance)


@receiver(pre_delete)
def blog_deleted_handler(instance, **kwargs):
    purge_related(instance)
