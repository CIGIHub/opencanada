from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch import urls as wagtailsearch_urls

from core.feeds import MainFeed
from core.views import chooser_search, site_search, template_error


base_urlpatterns = [
    url(r'^search/$', site_search, name='wagtailsearch_search'),
    url(r'^search/', include(wagtailsearch_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^', include('favicon.urls')),
    url(r'^', include('sitemap.urls')),
    url(r'^feed/$', MainFeed(), name='main_feed'),
    url(r'^error/$', lambda r: 1 / 0, name='error'),
    url(r'^template_error/$', template_error, name='template_error'),
    url(r'^core/', include('core.urls', namespace='core')),
    url(r'^robots\.txt', include('robots.urls')),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    base_urlpatterns += staticfiles_urlpatterns()
    base_urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    base_urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    base_urlpatterns += [
        url(r'^django-admin/', include(admin.site.urls)),
        url(r'^admin/choose-page/search/', chooser_search, name="wagtailadmin_choose_page_search"),
        url(r'^admin/', include(wagtailadmin_urls)),
        url(r'^500/$', 'django.views.defaults.server_error'),
        url(r'^404/$', TemplateView.as_view(template_name='404.html')),
        url(r'^403/$', TemplateView.as_view(template_name='403.html')),
    ]

urlpatterns = base_urlpatterns + [
    url(r'', include(wagtail_urls)),
]
