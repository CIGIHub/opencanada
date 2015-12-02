from __future__ import absolute_import

from django.conf import settings
from django.conf.urls import url
from django.contrib import messages
from django.core import management
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.html import format_html, format_html_join
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'span': attribute_rule({'data-target': True, 'data-toggle': True, 'class': True}),
    }


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'js/editor/hallo-supsub-plugin.js',
        'js/editor/hallo-modallink-plugin.js',
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
            'hallowagtaillink': {},
            'hallorequireparagraphs': {}
        };

        registerHalloPlugin('hallosupsub');
        registerHalloPlugin('hallomodallink');

        </script>
    """


@hooks.register('insert_editor_css')
def editor_css():
    return format_html('<link rel="stylesheet" href="'
                       + settings.STATIC_URL
                       + 'css/font-awesome.min.css">')


class LogoutLinkItem(object):
    def render(self, request):
        return '<li><a href="' + reverse('wagtailadmin_logout') + \
               '" target="_parent" class="action icon icon-redirect">Logout</a></li>'


@hooks.register('construct_wagtail_userbar')
def add_logout_link_item(request, items):
    return items.append(LogoutLinkItem())


def rebuild_search_index_view(request):
    if request.method == 'POST':
        management.call_command('update_index')
        messages.info(request, "The search index was rebuilt")
        return redirect('wagtailadmin_home')

    return render(
        request,
        'wagtailadmin/search/rebuild.html'
    )


@hooks.register('register_admin_urls')
def urlconf_time():
    return [
        url(r'^rebuild_search/$', rebuild_search_index_view, name='admin_rebuild_search'),
    ]


@hooks.register('register_admin_menu_item')
def register_frank_menu_item():
    return MenuItem('Rebuild Search', reverse('admin_rebuild_search'), classnames='icon icon-tag', order=10000)
