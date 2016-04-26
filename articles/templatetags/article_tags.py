import json
import urllib

from django import template
from django.utils.text import slugify

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


# Should only be called from a page template not a block template since we expect the context to contain the article
@register.simple_tag(takes_context=True)
def get_chapter_anchor(context, chapter):
    try:
        page = context["self"]
        article = page.articlepage
        block = chapter.value
        chapter_heading = block['heading']
    except ArticlePage.DoesNotExist:
        anchor = ''
    else:
        anchor = '{0}#{1}'.format(article.full_url[:-1], slugify(chapter_heading))
    return anchor


# Should only be called from a page template not a block template since we expect the context to contain the article
@register.simple_tag(takes_context=True)
def get_twitter_share_url(context, chapter):
    try:
        anchor = get_chapter_anchor(context, chapter)
    except ArticlePage.DoesNotExist:
        twitter_share_url = ''
    else:
        stream_field_value = chapter.value
        tweet_text = stream_field_value['tweet_text']
        twitter_share_params = []
        text = []
        _hashtags = set([])
        tweet_text_parts = tweet_text.split(' ')
        for word in tweet_text_parts:
            if len(word) > 0 and word[0] == '#':
                _hashtags.add(word[1:])
            text.append(word)
        if len(text) > 0:
            text = ' '.join(text)
            twitter_share_params.append('text={0}'.format(urllib.quote_plus(text)))
        if len(_hashtags) > 0:
            # You can collect hashtags and pass them along as a separate param...
            # However, doing so in this manner appends the hashtags to the end of the tweet, which we don't need to do
            # as the hashtags we want will already be in the tweet_text
            _hashtags = ','.join(_hashtags)
            twitter_share_params.append('hashtags={0}'.format(urllib.quote_plus(_hashtags)))
        twitter_share_params.append('url={0}'.format(urllib.quote_plus(anchor)))
        twitter_share_params = '&amp;'.join(twitter_share_params)
        twitter_share_url = 'https://twitter.com/share?{0}'.format(twitter_share_params)
    return twitter_share_url
