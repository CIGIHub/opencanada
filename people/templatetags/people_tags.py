from django import template

from articles.models import ArticlePage

register = template.Library()


@register.filter(name='contributor_articles')
def contributor_articles(contributor_page, number=None):
    articles = ArticlePage.objects.filter(author_links__author=contributor_page)
    if number:
        articles = articles[:number]
    return articles
