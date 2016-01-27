from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, ObjectList,
                                                TabbedInterface)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from core.base import PaginatedListPageMixin
from themes.models import ThemeablePage


@python_2_unicode_compatible
class Organization(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(max_length=255)
    logo = models.ForeignKey(
        'images.AttributedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.name


register_snippet(Organization)


Organization.panels = [
    FieldPanel('name'),
    FieldPanel('website'),
    ImageChooserPanel('logo'),
]


class EventListPage(PaginatedListPageMixin, ThemeablePage):
    subpage_types = ['EventPage']

    events_per_page = models.IntegerField(default=20)
    counter_field_name = 'events_per_page'
    counter_context_name = 'events'

    @property
    def subpages(self):
        # Get list of live event pages that are descendants of this page
        subpages = EventPage.objects.live().descendant_of(self).order_by('-date')

        return subpages

    content_panels = Page.content_panels + [
        FieldPanel('events_per_page')
    ]

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


@python_2_unicode_compatible
class EventPage(ThemeablePage):
    date = models.DateTimeField("Event Date")
    location = models.CharField(max_length=255)
    event_link = models.URLField(max_length=255)
    body = RichTextField()
    organization = models.ForeignKey(
        'Organization',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return "{}".format(
            self.title
        )

    def __init__(self, *args, **kwargs):
        super(EventPage, self).__init__(*args, **kwargs)
        for field in self._meta.fields:
            if field.name == 'first_published_at':
                field.editable = True
                field.blank = True

    content_panels = [
        FieldPanel("title"),
        FieldPanel("date"),
        FieldPanel("location"),
        FieldPanel("event_link"),
        FieldPanel("body"),
        SnippetChooserPanel('organization', Organization),
    ]

    style_panels = ThemeablePage.style_panels

    settings_panels = [FieldPanel('first_published_at'), ] + Page.settings_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(settings_panels, heading='Settings', classname="settings"),
    ])
