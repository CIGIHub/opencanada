from django import template
from django.db.models import ObjectDoesNotExist

from articles.models import Topic

register = template.Library()


@register.assignment_tag
def suggested_searches(number_of_suggestions):
    search_suggestions = Topic.objects.all().order_by('article_links__article__first_published_at')[:number_of_suggestions]

    return search_suggestions


@register.filter
def search_string(topic):
    return topic.name.replace(" ", "+")


@register.assignment_tag(takes_context=True)
def get_site_defaults(context):
    try:
        return context['request'].site.default_settings
    except ObjectDoesNotExist:
        return None
