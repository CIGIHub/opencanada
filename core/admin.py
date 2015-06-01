from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from . import models

admin.site.register(models.LegacyArticlePage)
admin.site.register(models.ArticlePage)
