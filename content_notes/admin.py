from django.contrib import admin

from . import models


class EndNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid')


admin.site.register(models.EndNote, EndNoteAdmin)
