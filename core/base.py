import logging
import os
import re
from datetime import timedelta
from urlparse import urlparse, urlunparse

import requests
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

logger = logging.getLogger('OpenCanada.CoreBaseModels')


class PaginatedListPageMixin(object):
    '''
    To use this mixing you need to define counter_field_name as the name of the field with
    the items per page and counter_context_name for the template. See jobs/models.py for an example
    '''
    def get_paginator(self, objects=None):
        if objects is None:
            objects = self.subpages
        return Paginator(objects, getattr(self, self.counter_field_name))

    def get_context(self, request):
        page = request.GET.get('page')
        paginator = self.get_paginator()

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context = super(PaginatedListPageMixin, self).get_context(request)
        context[self.counter_context_name] = objects
        return context

    def get_cached_paths(self):
        yield '/'

        # Yield one URL per page in the paginator to make sure all pages are purged
        for page_number in range(2, self.get_paginator().num_pages + 1):
            yield '/?page=' + str(page_number)


class ShareLinksMixin(models.Model):
    cached_twitter_count = models.IntegerField(default=0)
    cached_facebook_count = models.IntegerField(default=0)
    cached_last_updated = models.DateTimeField(blank=True, null=True)

    def _get_twitter_count(self):
        try:

            urls = ["https://opencanada.org{}".format(self.url), "http://opencanada.org{}".format(self.url), "https://www.opencanada.org{}".format(self.url)]
            total_shares = 0
            for page_url in urls:
                url = 'https://cdn.api.twitter.com/1/urls/count.json?url={}'.format(page_url)
                response = requests.get(url, timeout=5)
                j = response.json()
                total_shares += j.get('count', 0)
            return total_shares
        except requests.exceptions.RequestException:
            logger.error('There was an error getting the Twitter share count.', exc_info=True, extra={"page": self})
            return 0

    def _get_facebook_count(self):
        try:
            url = 'https://graph.facebook.com/?ids=https://opencanada.org{0},http://opencanada.org{0}'.format(self.url)
            response = requests.get(url, timeout=5)
            j = response.json()
            total_shares = 0
            for key, values in j.iteritems():
                total_shares += values.get('shares', 0)
            return total_shares
        except requests.exceptions.RequestException:
            logger.error('There was an error getting the Facebook share count.', exc_info=True, extra={"page": self})
            return 0

    def update_cache(self):
        if not self.cached_last_updated or (timezone.now() - self.cached_last_updated) > timedelta(minutes=10):
            tweet_count = self._get_twitter_count()
            if tweet_count > 0:
                self.cached_twitter_count = tweet_count

            facebook_count = self._get_facebook_count()
            if facebook_count > 0:
                self.cached_facebook_count = facebook_count

            self.cached_last_updated = timezone.now()
            self.save()

    @property
    def twitter_count(self):
        return self.cached_twitter_count

    @property
    def facebook_count(self):
        return self.cached_facebook_count

    class Meta:
        abstract = True


class VideoDocumentMixin(models.Model):
    video_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def get_video_src(self):
        url_parts = urlparse(self.video_document.url)
        try:
            domain = settings.AWS_S3_CUSTOM_DOMAIN
            path_parts = os.path.split(url_parts.path)
            filename = path_parts[-1]
            url_parts = ('https', domain, os.path.join('documents', filename), '', '', '')
        except AttributeError:
            # Assume local path
            pass
        return urlunparse(url_parts)

    class Meta:
        abstract = True


class UniquelySlugable(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:255]

            while type(self).objects.filter(slug=self.slug).exists():
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + "-" + str(next_int)
                else:
                    self.slug += '-2'

        super(UniquelySlugable, self).save(*args, **kwargs)
