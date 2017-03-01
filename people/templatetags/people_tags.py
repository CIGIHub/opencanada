from django import template

from articles.models import ArticlePage

register = template.Library()


@register.simple_tag()
def contributor_articles(contributor_page, article_page_id=None, number=None):
    if article_page_id:
        articles = ArticlePage.objects.live().filter(author_links__author=contributor_page).exclude(id=article_page_id).order_by("-first_published_at")
    else:
        articles = ArticlePage.objects.live().filter(author_links__author=contributor_page).order_by("-first_published_at")
    if number:
        articles = articles[:number]
    return articles
