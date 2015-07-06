from django.contrib import admin

from . import models

admin.site.register(models.AttributedImage)
admin.site.register(models.AttributedRendition)
