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

@register.filter
def get_video_src(url):
    import os
    from urlparse import urlparse, urlunparse
    from django.conf import settings
    url_parts = urlparse(url)
    try:
        domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN')
        path_parts = os.path.split(url_parts.path)
        filename = path_parts[-1]
        url_parts = ('https', domain, os.path.join('documents', filename), '', '', '')
    except AttributeError:
        # Assume local path
        pass
    return urlunparse(url_parts)

@register.tag
def value_from_settings(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError("'%s' takes at least one argument (settings constant to retrieve)" % bits[0])
    settingsvar = bits[1]
    settingsvar = settingsvar[1:-1] if settingsvar[0] == '"' else settingsvar
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]
    if len(bits):
        raise template.TemplateSyntaxError("'value_from_settings' didn't recognise the arguments '%s'" % ", ".join(bits))
    return ValueFromSettings(settingsvar, asvar)

class ValueFromSettings(template.Node):
    def __init__(self, settingsvar, asvar):
        self.arg = template.Variable(settingsvar)
        self.asvar = asvar

    def render(self, context):
        from django.conf import settings
        ret_val = getattr(settings, str(self.arg), 'http://example.com')
        if self.asvar:
            context[self.asvar] = ret_val
            return ''
        else:
            return ret_val