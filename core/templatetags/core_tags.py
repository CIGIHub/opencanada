from django import template

from core.models import SearchSuggestion

register = template.Library()


@register.assignment_tag
def suggested_searches(number_of_suggestions):
    search_suggestions = SearchSuggestion.objects.filter(active=True)[:number_of_suggestions]

    return search_suggestions
