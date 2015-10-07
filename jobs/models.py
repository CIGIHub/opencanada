from django.db import models
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, ObjectList,
                                                RichTextFieldPanel,
                                                TabbedInterface)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page

from core.base import PaginatedListPageMixin, ShareLinksMixin
from themes.models import ThemeablePage


class JobPostingPage(ThemeablePage, ShareLinksMixin):
    body = RichTextField()

    content_panels = Page.content_panels + [
        RichTextFieldPanel('body'),
    ]

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


class JobPostingListPage(PaginatedListPageMixin, ThemeablePage):
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

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])
