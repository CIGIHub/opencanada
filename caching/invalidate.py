from __future__ import absolute_import, unicode_literals

import logging

import requests
from django.conf import settings
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
from six.moves import xrange

logger = logging.getLogger(__name__)

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

    # articles_models.ChapteredArticlePage: [
    #     articles_models.ArticleListPage,
    #     articles_models.TopicListPage,
    #     articles_models.SeriesListPage,
    #     HomePage,
    # ],

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


_cloudflare_config = None


def get_cloudflare_config():
    global _cloudflare_config
    if _cloudflare_config is None:
        config = getattr(settings, 'WAGTAILFRONTENDCACHE', None)
        if config is None:
            logger.error('Configuration Error: WAGTAILFRONTENDCACHE expected in settings. Cache not invalidated.')
            return None

        if 'cloudflare' not in config:
            logger.error('Configuration Error: Key "cloudflare" expected in WAGTAILFRONTENDCACHE setting. Cache not invalidated.')
            return None

        _cloudflare_config = config['cloudflare']

    return _cloudflare_config


def cloudflare_request(method, url, data):
    cloudflare_config = get_cloudflare_config()

    if cloudflare_config is None:
        return

    url_base = 'https://api.cloudflare.com/client/v4'
    url = url_base + url.format(**cloudflare_config)

    headers = {
        'X-Auth-Email': cloudflare_config['EMAIL'],
        'X-Auth-Key': cloudflare_config['TOKEN'],
    }

    print(method, url, data)
    resp = method(url, json=data, headers=headers)
    try:
        resp_json = resp.json()
    except ValueError:
        logger.error('Cloudflare API Error: Unable to parse response into JSON. {}'.format(resp.content))
        return None

    if resp_json['success'] is False:
        logger.error('Cloudflare API Error: Request did not succeed. {}'.format(resp_json))
        return None

    return resp


def cloudflare_purge_all():
    data = {"purge_everything": True}

    cloudflare_request(
        requests.delete,
        '/zones/{ZONE_ID}/purge_cache',
        data,
    )


# From http://stackoverflow.com/a/434328/91243
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))


def cloudflare_purge_urls(urls):
    if not isinstance(urls, list):
        urls = [urls]

    for urls in chunker(urls, 30):
        data = {"files": urls}

        cloudflare_request(
            requests.delete,
            '/zones/{ZONE_ID}/purge_cache',
            data,
        )


def purge_related(instance):
    global invalidation_map
    instance_model = instance.__class__
    if instance_model not in invalidation_map:
        return
    for related_page_model in invalidation_map[instance_model]:
        for page in related_page_model.objects.live():
            print("Purging {}".format(page))
            purge_page_from_cache(page)


@receiver(page_published)
def page_published_handler(instance, **kwargs):
    cloudflare_purge_all()
    # purge_related(instance)


@receiver(pre_delete)
def page_deleted_handler(instance, **kwargs):
    cloudflare_purge_all()
    # purge_related(instance)
