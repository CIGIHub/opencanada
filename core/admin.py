from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from wagtail.core.models import PageRevision
from wagtail.embeds.models import Embed

from . import models

admin.site.register(models.HomePage)
admin.site.register(PageRevision)
admin.site.register(Embed)
