from django import template

from articles.models import ArticlePage

register = template.Library()


@register.assignment_tag()
def contributor_articles(contributor_page, article_page_id, number=None):
    articles = ArticlePage.objects.filter(author_links__author=contributor_page).exclude(id=article_page_id)
    if number:
        articles = articles[:number]
    return articles
