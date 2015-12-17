from __future__ import absolute_import, division, unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from wagtail.wagtailadmin.edit_handlers import (ObjectList, RichTextFieldPanel,
                                                TabbedInterface)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index

from themes.models import ThemeablePage


class ProjectListPage(ThemeablePage):
    subpage_types = ['ProjectPage']

    @property
    def subpages(self):
        subpages = ProjectPage.objects.live().descendant_of(self).order_by('title')
        return subpages

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


@python_2_unicode_compatible
class ProjectPage(ThemeablePage):
    description = RichTextField(blank=True, default="")

    search_fields = Page.search_fields + (
        index.SearchField('description', partial_match=True),
    )

    def search_result_text(self):
        if self.description:
            self.search_result_text = self.description[0:240]
        return self.search_result_text

    def project_articles(self):
        return self.articlepage_set.live().order_by("-first_published_at")

    def __str__(self):
        return "{}".format(
            self.title
        )

    content_panels = Page.content_panels + [
        RichTextFieldPanel('description'),
    ]

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])
