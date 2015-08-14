from django import template

from articles.models import ArticlePage

register = template.Library()


@register.assignment_tag()
def contributor_articles(contributor_page, article_page_id=None, number=None):
    if article_page_id:
        articles = ArticlePage.objects.live().filter(author_links__author=contributor_page).exclude(id=article_page_id)
    else:
        articles = ArticlePage.objects.live().filter(author_links__author=contributor_page)
    if number:
        articles = articles[:number]
    return articles
