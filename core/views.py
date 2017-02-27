from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from wagtail.utils.pagination import paginate
from wagtail.wagtailadmin.forms import SearchForm
from wagtail.wagtailadmin.views.chooser import (filter_page_type,
                                                page_models_from_string,
                                                shared_context)
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query
from wagtail.wagtailsearch.views import search


def social_share_count(request, page_id):

    page = Page.objects.specific().get(id=page_id)

    page.update_cache()

    twitter_shares = page.twitter_count
    facebook_shares = page.facebook_count
    return JsonResponse({'twitter': twitter_shares,
                         'facebook': facebook_shares})


# This was taken from wagtailadmin/views/chooser.py. There isn't a clear way to override this behavior.
# As is this is a maintenance headache, but one which is probably worth it. Check for changes to this
# function in choose.py when wagtail releases new versions
def chooser_search(request, parent_page_id=None):
    # A missing or empty page_type parameter indicates 'all page types' (i.e. descendants of wagtailcore.page)
    page_type_string = request.GET.get('page_type') or 'wagtailcore.page'

    try:
        desired_classes = page_models_from_string(page_type_string)
    except (ValueError, LookupError):
        raise Http404

    search_form = SearchForm(request.GET)
    if search_form.is_valid() and search_form.cleaned_data['q']:
        pages = Page.objects.exclude(
            depth=1  # never include root
        ).order_by('-first_published_at')  # change 1) give pages a default order
        pages = filter_page_type(pages, desired_classes)
        pages = pages.search(search_form.cleaned_data['q'], fields=['title'], order_by_relevance=False, operator='and')  # change 2) order by the new default order
    else:
        pages = Page.objects.none()

    paginator, pages = paginate(request, pages, per_page=25)

    for page in pages:
        page.can_choose = True

    return render(
        request, 'wagtailadmin/chooser/_search_results.html',
        shared_context(request, {
            'searchform': search_form,
            'pages': pages,
            'page_type_string': page_type_string,
        })
    )


def site_search(request, template=None, results_per_page=10, path=None):
    # Get default templates
    if template is None:
        if hasattr(settings, 'WAGTAILSEARCH_RESULTS_TEMPLATE'):
            template = settings.WAGTAILSEARCH_RESULTS_TEMPLATE
        else:
            template = 'wagtailsearch/search_results.html'

    # Get query string and page from GET paramters
    query_string = request.GET.get('q', '')
    page = request.GET.get('page', request.GET.get('p', 1))
    if '"' not in query_string:
        return search(request, template=template, results_per_page=results_per_page, path=path)

    # Special quoted search
    pages = Page.objects.filter(path__startswith=(path or request.site.root_page.path))

    search_results = pages.search(query_string.replace('"', ''), operator='and')

    # Get query object
    query = Query.get(query_string)

    # Add hit
    query.add_hit()

    # Pagination
    paginator = Paginator(search_results, results_per_page)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, template, dict(
        query_string=query_string,
        search_results=search_results,
        is_ajax=request.is_ajax(),
        query=query
    ))


def template_error(request):
    from django.template import Template, Context

    template = Template("This is for testing template {% include 'template_error.html' %}")
    content = template.render(Context(dict(foo="bar")))
    return HttpResponse(content)
