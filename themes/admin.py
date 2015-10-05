from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from . import models

admin.site.register(models.LogoBlock)
admin.site.register(models.TextBlock)
admin.site.register(models.FollowLink)
admin.site.register(models.Menu)
admin.site.register(models.MenuItem)
admin.site.register(models.ThemeContent)
admin.site.register(models.Theme)
