from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls

from core.views import chooser_search

from .urls import base_urlpatterns

urlpatterns = base_urlpatterns + [
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^admin/choose-page/search/', chooser_search, name="wagtailadmin_choose_page_search"),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'', include(wagtail_urls)),
]
