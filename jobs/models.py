from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel, RichTextFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page

from core.base import ListPageMixin


class JobPostingPage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        RichTextFieldPanel('body'),
    ]


class JobPostingListPage(ListPageMixin, Page):
    subpage_types = [
        'JobPostingPage',
    ]

    jobs_per_page = models.IntegerField(default=10)
    counter_field_name = 'jobs_per_page'
    counter_context_name = 'jobs'

    @property
    def subpages(self):
        subpages = JobPostingPage.objects.live().order_by('-first_published_at')
        return subpages

    content_panels = Page.content_panels + [
        FieldPanel('jobs_per_page'),
    ]
