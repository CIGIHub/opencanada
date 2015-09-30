from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils.translation import ugettext as _
from wagtail.wagtailadmin.forms import SearchForm
from wagtail.wagtailsearch.backends import get_search_backend
from wagtail.wagtailsearch.index import class_is_indexed

from ..models import EndNote


# == Views ==

def list(request):

    items = EndNote.objects.all()

    # Search
    is_searchable = class_is_indexed(EndNote)
    is_searching = False
    search_query = None
    if is_searchable and 'q' in request.GET:
        search_form = SearchForm(request.GET, placeholder=_("Search End Notes"))

        if search_form.is_valid():
            search_query = search_form.cleaned_data['q']

            search_backend = get_search_backend()
            items = search_backend.search(search_query, items)
            is_searching = True

    else:
        search_form = SearchForm(placeholder=_("Search End Notes"))

    # Pagination
    p = request.GET.get('p', 1)
    paginator = Paginator(items, 20)

    try:
        paginated_items = paginator.page(p)
    except PageNotAnInteger:
        paginated_items = paginator.page(1)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)

    # Template
    if request.is_ajax():
        template = 'content_notes/endnotes/results.html'
    else:
        template = 'content_notes/endnotes/type_index.html'

    return render(request, template, {
        'items': paginated_items,
        'is_searchable': is_searchable,
        'search_form': search_form,
        'is_searching': is_searching,
        'query_string': search_query,
    })
