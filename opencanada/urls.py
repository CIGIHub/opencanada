from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.defaults import server_error

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.search import urls as wagtailsearch_urls

from core.feeds import MainFeed
from core.views import chooser_search, site_search, template_error

base_urlpatterns = [
    re_path(r'^search/$', site_search, name='wagtailsearch_search'),
    re_path(r'^search/', include(wagtailsearch_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'^', include('favicon.urls')),
    re_path(r'^', include('sitemap.urls')),
    re_path(r'^feed/$', MainFeed(), name='main_feed'),
    re_path(r'^error/$', lambda r: 1 / 0, name='error'),
    re_path(r'^template_error/$', template_error, name='template_error'),
    re_path(r'^core/', include('core.urls')),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    base_urlpatterns += staticfiles_urlpatterns()
    base_urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    base_urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    base_urlpatterns += [
        path('django-admin/', admin.site.urls),
        re_path(r'^admin/choose-page/search/', chooser_search, name="wagtailadmin_choose_page_search"),
        re_path(r'^admin/', include(wagtailadmin_urls)),
        re_path(r'^500/$', server_error),
        re_path(r'^404/$', TemplateView.as_view(template_name='404.html')),
        re_path(r'^403/$', TemplateView.as_view(template_name='403.html')),
    ]

    # import debug_toolbar
    # base_urlpatterns = [
    #     re_path(r'^__debug__/', include(debug_toolbar.urls)),
    # ] + base_urlpatterns

urlpatterns = base_urlpatterns + [
    re_path(r'', include(wagtail_urls)),
]
