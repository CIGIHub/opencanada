from django import template
from django.db.models import ObjectDoesNotExist

from jobs.models import JobPostingListPage

register = template.Library()


@register.simple_tag(takes_context=True)
def get_active_posting_page(context):
    try:
        root = context['request'].site.root_page
        listing_pages = JobPostingListPage.objects.descendant_of(root)

        if listing_pages.count() > 0:
            listing_page = listing_pages[0]

            if listing_page.subpages.count() > 0:
                if listing_page.subpages.count() == 1:
                    return listing_page.subpages[0]

                return listing_page

            return None

    except ObjectDoesNotExist:
        return None
