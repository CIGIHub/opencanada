from itertools import chain
from operator import attrgetter

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy

from articles.models import ArticlePage, SeriesPage


class MainFeed(Feed):
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
