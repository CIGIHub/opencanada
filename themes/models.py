from __future__ import absolute_import, division, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


def get_default_theme():
    return Theme.objects.filter(is_default=True).order_by('id').first()


@python_2_unicode_compatible
class Theme(models.Model):
    name = models.CharField(max_length=1024)
    folder = models.CharField(max_length=1024, default="themes/default")
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

register_snippet(Theme)


class ThemeablePage(Page):
    is_creatable = False

    class Meta:
        abstract = True

    theme = models.ForeignKey(Theme,
                              default=get_default_theme,
                              on_delete=models.SET_NULL,
                              null=True)

    def get_template(self, request, *args, **kwargs):
        original_template = super(ThemeablePage, self).get_template(request, *args, **kwargs)
        if self.theme:
            return "{}/{}".format(self.theme.folder, original_template)
        else:
            return original_template

    style_panels = [
        MultiFieldPanel(
            [
                SnippetChooserPanel('theme', Theme),
            ],
            heading="Theme"
        ),
    ]
