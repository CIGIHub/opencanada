import os

from django import template
from django.conf import settings
from django.db.models import ObjectDoesNotExist
from six.moves.urllib.parse import urlparse

from articles.models import Topic

from ..models import SiteDefaults

register = template.Library()


@register.simple_tag
def suggested_searches(number_of_suggestions):
    search_suggestions = Topic.objects.all().order_by('article_links__article__first_published_at')[:number_of_suggestions]

    return search_suggestions


@register.filter
def search_string(topic):
    return topic.name.replace(" ", "+")


@register.simple_tag(takes_context=True)
def get_site_defaults(context):
    try:
        return context['request'].site.default_settings
    except (AttributeError, ObjectDoesNotExist) as e:
        return SiteDefaults.objects.get(site__is_default_site=True)


@register.simple_tag(takes_context=True)
def external_article_image(context, item):
    if hasattr(item, "source"):
        if item.source and item.source.logo:
            return item.source.logo
        else:
            try:
                default_settings = context['request'].site.default_settings
                return default_settings.default_external_article_source_logo
            except ObjectDoesNotExist:
                pass
    return item.main_image


@register.filter
def media(url):
    media_url = url
    url_is_absolute = bool(urlparse(url).netloc)
    if not url_is_absolute:
        media_url = os.path.join(settings.MEDIA_URL, url)
    return media_url


@register.filter
def error(v):
    '''
    Warrning, for testing purposes only
    '''
    error_value = 1 / 0
    return error_value
