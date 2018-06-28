from __future__ import absolute_import, unicode_literals

import logging
import re

from django import template
from django.conf import settings
from wagtail.images.templatetags.wagtailimages_tags import ImageNode

register = template.Library()
allowed_filter_pattern = re.compile("^[A-Za-z0-9_\-\.]+$")
logger = logging.getLogger(__name__)


# MAINTAINANCE WARNING
# I really only want to override the ImageNode's render method, but the tag itself
# wraps the construction of the Node class in a way that isn't overridable, so I
# had to copy the whole image tag function from
# wagtail/wagtailimages/template_tags/wagtailimages_tags.py.
@register.tag(name="image")
def image(parser, token):
    bits = token.split_contents()[1:]
    image_expr = parser.compile_filter(bits[0])
    bits = bits[1:]

    filter_specs = []
    attrs = {}
    output_var_name = None

    as_context = False  # if True, the next bit to be read is the output variable name
    is_valid = True

    for bit in bits:
        if bit == 'as':
            # token is of the form {% image self.photo max-320x200 as img %}
            as_context = True
        elif as_context:
            if output_var_name is None:
                output_var_name = bit
            else:
                # more than one item exists after 'as' - reject as invalid
                is_valid = False
        else:
            try:
                name, value = bit.split('=')
                attrs[name] = parser.compile_filter(value)  # setup to resolve context variables as value
            except ValueError:
                if allowed_filter_pattern.match(bit):
                    filter_specs.append(bit)
                else:
                    raise template.TemplateSyntaxError(
                        "filter specs in 'image' tag may only contain A-Z, a-z, 0-9, dots, hyphens and underscores. "
                        "(given filter: {})".format(bit)
                    )

    if as_context and output_var_name is None:
        # context was introduced but no variable given ...
        is_valid = False

    if output_var_name and attrs:
        # attributes are not valid when using the 'as img' form of the tag
        is_valid = False

    if is_valid:
        return OCImageNode(image_expr, '|'.join(filter_specs), attrs=attrs, output_var_name=output_var_name)  # One line with a change
    else:
        raise template.TemplateSyntaxError(
            "'image' tag should be of the form {% image self.photo max-320x200 [ custom-attr=\"value\" ... ] %} "
            "or {% image self.photo max-320x200 as img %}"
        )


class OCImageNode(ImageNode):
    def render(self, context):
        debug = getattr(settings, 'DEBUG', False)
        try:
            return super(OCImageNode, self).render(context)
        except Exception:
            if debug:
                raise
            else:
                logger.exception("Unexpected issue rendering image.")
                return ''
