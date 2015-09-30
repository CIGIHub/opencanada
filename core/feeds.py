from __future__ import absolute_import, unicode_literals

from itertools import chain
from operator import attrgetter

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.utils.feedgenerator import Rss201rev2Feed

from articles.models import ArticlePage, SeriesPage


# Based on http://www.mechanicalgirl.com/post/customizing-django-rss-feed/
class FeedlyRSSFeed(Rss201rev2Feed):
    def rss_attributes(self):
        attrs = super(FeedlyRSSFeed, self).rss_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        attrs['xmlns:webfeeds'] = 'http://webfeeds.org/rss/1.0'
        return attrs

    def add_root_elements(self, handler):
        super(FeedlyRSSFeed, self).add_root_elements(handler)
        handler.addQuickElement(
            'webfeeds:logo',
            settings.BASE_URL + static('img/opencanada-logo-square.png'),
        )

        handler.addQuickElement(
            'webfeeds:accentColor',
            'bf1e2e',
        )

        if settings.GOOGLE_ANALYTICS_PROPERTY_ID:
            handler.addQuickElement(
                'webfeeds:analytics',
                attrs=dict(
                    id=settings.GOOGLE_ANALYTICS_PROPERTY_ID,
                    engine='GoogleAnalytics',
                )
            )


class MainFeed(Feed):
    feed_type = FeedlyRSSFeed
    title = "OpenCanada.org - All Articles RSS"
    link = '/'
    description = 'OpenCanada.org is a publication of the Canadian International Council, the Centre for International Governance Innovation and the Bill Graham Centre'
    feed_url = reverse_lazy('main_feed')

    description_template = 'feeds/main/description.html'

    def items(self):
        articles = ArticlePage.objects.order_by('-first_published_at')[:50]
        series = SeriesPage.objects.order_by('-first_published_at')[:50]

        return list(reversed(
            sorted(
                chain(articles, series),
                key=attrgetter('first_published_at')
            )
        ))[:50]

    def item_title(self, obj):
        return obj.title

    def item_link(self, obj):
        return obj.full_url

    def item_author_name(self, obj):
        return (', ').join([author.title for author in obj.authors])

    def item_pubdate(self, obj):
        return obj.first_published_at
