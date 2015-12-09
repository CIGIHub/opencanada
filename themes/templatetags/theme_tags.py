from django import template
from django.db.models import ObjectDoesNotExist

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_contact_email(context):
    theme = get_theme(context)

    email = theme.content.contact_email
    if not email:
        try:
            defaults = context['request'].site.default_settings
            return defaults.contact_email
        except ObjectDoesNotExist:
            return ""

    return email


def get_theme(context):
    default_theme = context["default_theme"]
    try:
        page = context["self"]
        return page.theme
    except:
        return default_theme


@register.assignment_tag(takes_context=True)
def get_text_block(context, usage):
    theme = get_theme(context)
    return theme.content.block_links.filter(theme_content=theme.content, block__usage=usage).first().block


@register.assignment_tag(takes_context=True)
def get_follow_link(context, usage):
    theme = get_theme(context)
    return theme.content.follow_links.filter(theme_content=theme.content, block__usage=usage).first().block.link


@register.assignment_tag(takes_context=True)
def get_logo(context, usage):
    theme = get_theme(context)
    return theme.content.logo_links.filter(theme_content=theme.content, block__usage=usage).first().block.logo


@register.assignment_tag(takes_context=True)
def get_logo_link(context, usage):
    theme = get_theme(context)
    return theme.content.logo_links.filter(theme_content=theme.content, block__usage=usage).first().block.link


@register.assignment_tag(takes_context=True)
def get_json_data(context):
    theme = get_theme(context)
    return theme.content.json_file_as_object
