from django import template

from articles.models import TopicListPage

register = template.Library()


@register.filter(name='related_articles')
def related_articles(value, number):
    return value.related_articles(number)


@register.simple_tag(takes_context=True)
def topic_url(context, topic):
    request = context['request']
    page = TopicListPage.objects.get(slug='topics')
    base_url = page.relative_url(request.site)
    routed_url = page.reverse_subpage('topic', [topic.slug])
    return base_url + routed_url


@register.filter()
def column_class(row):
    number_of_items = len(row)
    return 12 / number_of_items
