from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from wagtail.wagtailcore.models import PageRevision

from . import models


class SearchSuggestionAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'active', )


admin.site.register(models.HomePage)
admin.site.register(PageRevision)
admin.site.register(models.SearchSuggestion, SearchSuggestionAdmin)
