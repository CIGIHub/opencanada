from __future__ import absolute_import

from django.conf import settings
from django.utils.html import format_html, format_html_join
from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_js')
def editor_js():

    js_files = [
        'js/editor/hallo-supsub-plugin.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
                                   ((settings.STATIC_URL, filename) for filename in js_files)
                                   )
    return js_includes + \
        """
        <script>

         halloPlugins = {
            'halloformat': {},
            'hallolists': {},
            'halloreundo': {},
            'hallolink': {},
            'hallowagtaillink': {},
            'hallorequireparagraphs': {}
        };

        registerHalloPlugin('hallosupsub');

        </script>
    """


@hooks.register('insert_editor_css')
def editor_css():
    return format_html('<link rel="stylesheet" href="'
                       + settings.STATIC_URL
                       + 'css/font-awesome.min.css">')
