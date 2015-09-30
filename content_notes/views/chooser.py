import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.utils.six import text_type
from django.utils.translation import ugettext as _
from wagtail.wagtailadmin.forms import SearchForm
from wagtail.wagtailadmin.modal_workflow import render_modal_workflow
from wagtail.wagtailsearch.backends import get_search_backend
from wagtail.wagtailsearch.index import class_is_indexed

from ..models import EndNote


def choose(request):
    # TODO: Ideally this would return the endnotes for the current article.
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
    p = request.GET.get("p", 1)
    paginator = Paginator(items, 25)

    try:
        paginated_items = paginator.page(p)
    except PageNotAnInteger:
        paginated_items = paginator.page(1)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)

    # If paginating or searching, render "results.html"
    if request.GET.get('results', None) == 'true':
        return render(request, "content_notes/chooser/results.html", {
            'items': paginated_items,
            'query_string': search_query,
            'is_searching': is_searching,
        })

    return render_modal_workflow(
        request,
        'content_notes/chooser/choose.html', 'content_notes/chooser/choose.js',
        {
            'items': paginated_items,
            'is_searchable': is_searchable,
            'search_form': search_form,
            'query_string': search_query,
            'is_searching': is_searching,
        }
    )


def chosen(request, id):
    item = get_object_or_404(EndNote, id=id)

    end_note_json = json.dumps({
        'id': item.uuid,
        'string': text_type(item)
    })

    return render_modal_workflow(
        request,
        None, 'content_notes/chooser/chosen.js',
        {
            'endnote_json': end_note_json,
        }
    )
