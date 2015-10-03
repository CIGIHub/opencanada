from django import template
from django.db.models import ObjectDoesNotExist

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_contact_email(context, theme):

    email = theme.footer_content.contact_email
    if not email:
        try:
            defaults = context['request'].site.default_settings
            return defaults.contact_email
        except ObjectDoesNotExist:
            return ""

    return email
