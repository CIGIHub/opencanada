from __future__ import absolute_import, unicode_literals

from django.urls import include, re_path
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls

from core.views import chooser_search

from .urls import base_urlpatterns

urlpatterns = base_urlpatterns + [
    re_path(r'^django-admin/', include(admin.site.urls)),
    re_path(r'^admin/choose-page/search/', chooser_search, name="wagtailadmin_choose_page_search"),
    re_path(r'^admin/', include(wagtailadmin_urls)),
    re_path(r'', include(wagtail_urls)),
]
