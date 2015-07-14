from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.ImageImport)
admin.site.register(models.PostImport)
admin.site.register(models.ImportDownloadError)
admin.site.register(models.TagImport)
