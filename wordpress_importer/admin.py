from django.contrib import admin

from . import models


class PostImportAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_permalink')


admin.site.register(models.ImageImport)
admin.site.register(models.PostImport, PostImportAdmin)
admin.site.register(models.ImportDownloadError)
admin.site.register(models.TagImport)
