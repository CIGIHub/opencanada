from django import template

from articles.models import ArticlePage

register = template.Library()


@register.assignment_tag()
def project_articles(project_page):
    articles = ArticlePage.objects.live().filter(project=project_page).order_by("-first_published_at")
    return articles
