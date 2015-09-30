
from django.conf import settings
from django.conf.urls import include, url
from django.core import urlresolvers
from django.utils.html import format_html
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule

from . import urls


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^content_notes/', include(urls, namespace='content_notes')),
    ]


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'sup': attribute_rule({'data-target': True, 'data-toggle': True, 'data-reference': True, 'class': True}),
    }


@hooks.register('insert_editor_js')
def editor_js():
    return format_html("""
            <script src="{0}{1}"></script>
            <script src="{0}{2}"></script>
            <script>window.chooserUrls.endNoteChooser = '{3}';</script>
            <script>
                registerHalloPlugin('halloendnotelink');
            </script>
        """,
                       settings.STATIC_URL,
                       'content_notes/js/end-note-chooser.js',
                       'content_notes/js/hallo-endnotelink-plugin.js',
                       urlresolvers.reverse('content_notes:choose')
                       )


@hooks.register('insert_editor_css')
def editor_css():
    return '<style> .hidden_input label{ display: none; } </style>'
