from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from wagtail.wagtailcore.models import PageRevision
from wagtail.wagtailembeds.models import Embed

from . import models

admin.site.register(models.HomePage)
admin.site.register(PageRevision)
admin.site.register(Embed)
