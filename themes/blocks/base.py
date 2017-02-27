from __future__ import absolute_import, unicode_literals

from django.template.loader import TemplateDoesNotExist, render_to_string
from wagtail.wagtailcore.blocks import StructBlock

# unicode_literals ensures that any render / __str__ methods returning HTML via calls to mark_safe / format_html
# return a SafeText, not SafeBytes; necessary so that it doesn't get re-encoded when the template engine
# calls force_text, which would cause it to lose its 'safe' flag


__all__ = ['ThemeableStructBlock']


class ThemeableStructBlock(StructBlock):
    def __init__(self, **kwargs):
        super(ThemeableStructBlock, self).__init__(**kwargs)
        self.theme = None

    def set_theme(self, theme):
        self.theme = theme

    def render(self, value, context=None):
        """
        Return a text rendering of 'value', suitable for display on templates. By default, this will
        use a template if a 'template' property is specified on the block, and fall back on render_basic
        otherwise.
        """
        template = getattr(self.meta, 'template', None)
        if template:
            if self.theme:
                theme_template = "{}/{}".format(self.theme.folder, template)
                try:
                    return render_to_string(theme_template, self.get_context(value))
                except TemplateDoesNotExist:
                    # Template for the Block does not exist in the Theme...
                    return render_to_string(template, self.get_context(value))
        else:
            return self.render_basic(value)
