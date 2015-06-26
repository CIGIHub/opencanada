from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.ArticlePage)
admin.site.register(models.ArticleListPage)
admin.site.register(models.Headline)
