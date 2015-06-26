from django import template

register = template.Library()


@register.filter(name='related_articles')
def related_articles(value, number):
    return value.related_articles(number)
