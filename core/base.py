from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class PaginatedListPageMixin(object):
    '''
    To use this mixing you need to define counter_field_name as the name of the field with
    the items per page and counter_context_name for the template. See jobs/models.py for an example
    '''
    def get_paginator(self, objects=None):
        if objects is None:
            objects = self.subpages
        return Paginator(objects, getattr(self, self.counter_field_name))

    def get_context(self, request):
        page = request.GET.get('page')
        paginator = self.get_paginator()

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context = super(PaginatedListPageMixin, self).get_context(request)
        context[self.counter_context_name] = objects
        return context

    def get_cached_paths(self):
        yield '/'

        # Yield one URL per page in the paginator to make sure all pages are purged
        for page_number in range(2, self.get_paginator().num_pages + 1):
            yield '/?page=' + str(page_number)
