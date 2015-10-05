from django import template
from django.db.models import ObjectDoesNotExist

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_contact_email(context, theme):

    email = theme.content.contact_email
    if not email:
        try:
            defaults = context['request'].site.default_settings
            return defaults.contact_email
        except ObjectDoesNotExist:
            return ""

    return email


@register.filter
def get_text_block(theme, slug):
    return theme.content.block_links.filter(theme_content=theme.content, block__slug=slug).first().block


@register.filter
def get_follow_link(theme, slug):
    return theme.content.follow_links.filter(theme_content=theme.content, block__slug=slug).first().block.link


@register.filter
def get_logo(theme, slug):
    return theme.content.logo_links.filter(theme_content=theme.content, block__slug=slug).first().block.logo
