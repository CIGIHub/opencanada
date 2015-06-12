from __future__ import absolute_import, unicode_literals

from wagtail.wagtailadmin.edit_handlers import FieldPanel, RichTextFieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.models import register_snippet

from people import models as people_models


class HomePage(Page):
    pass


register_snippet(people_models.Contributor)

people_models.Contributor.panels = [
    FieldPanel('first_name'),
    FieldPanel('last_name'),
    FieldPanel('nickname'),
    FieldPanel('email'),
    FieldPanel('twitter_handle'),
    RichTextFieldPanel('short_bio'),
    RichTextFieldPanel('long_bio'),
]
