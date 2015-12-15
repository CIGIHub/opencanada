import json

from django import template

from articles.models import (ArticlePage, ExternalArticlePage, SeriesPage,
                             TopicListPage)

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


@register.filter()
def column_height(article):
    return article.feature_style.number_of_rows * 280


@register.filter()
def get_feature_image(item):
    if item.feature_image:
        return item.feature_image
    else:
        return item.main_image


@register.assignment_tag()
def typed_article(page):
    try:
        return page.articlepage
    except ArticlePage.DoesNotExist:
        pass

    try:
        return page.seriespage
    except SeriesPage.DoesNotExist:
        pass

    try:
        return page.externalarticlepage
    except ExternalArticlePage.DoesNotExist:
        pass

    return page


@register.filter()
def romanize(value):

    try:
        value = int(value)
    except ValueError:
        raise TypeError("expected integer, got {}".format(type(value)))
    if not (0 < value < 4000):
        raise ValueError("Argument must be between 1 and 3999")

    number_map = (('m', 1000),
                  ('cm', 900),
                  ('d', 500),
                  ('cd', 400),
                  ('c', 100),
                  ('xc', 90),
                  ('l', 50),
                  ('xl', 40),
                  ('x', 10),
                  ('ix', 9),
                  ('v', 5),
                  ('iv', 4),
                  ('i', 1),
                  )
    result = ""
    for numeral, integer in number_map:
        while value >= integer:
            result += numeral
            value -= integer

    return result


@register.assignment_tag(takes_context=True)
def get_json_data(context):
    try:
        page = context["self"]
        article = page.articlepage
    except ArticlePage.DoesNotExist:
        pass
    else:
        if article.json_file:
            json_object = json.load(article.json_file)
            return json_object

