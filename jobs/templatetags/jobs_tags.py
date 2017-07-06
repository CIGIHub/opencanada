from django import template

from jobs.models import JobPostingListPage, JobPostingPage

register = template.Library()


@register.simple_tag(takes_context=True)
def get_active_posting_page(context):
    # This used to be more complex pre July 2017 to support multiple roots
    # but that functionality is not longer required.
    if JobPostingPage.objects.live().count() == 0:
        return None

    listing_page = JobPostingListPage.objects.live().first()
    return listing_page
