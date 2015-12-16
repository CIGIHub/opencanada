from django import template

from articles.models import ArticlePage

register = template.Library()


@register.assignment_tag()
def related_pages(project_page):
    articles = ArticlePage.objects.live().filter(project=project_page)
    return articles
