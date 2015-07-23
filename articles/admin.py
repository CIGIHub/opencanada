from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.ArticlePage)
admin.site.register(models.ArticleListPage)
admin.site.register(models.Headline)
admin.site.register(models.Colour)
admin.site.register(models.ArticleAuthorLink)
admin.site.register(models.ArticleCategory)
admin.site.register(models.ArticleTopicLink)
admin.site.register(models.FeatureStyle)
admin.site.register(models.FontStyle)
admin.site.register(models.SeriesArticleLink)
admin.site.register(models.SeriesListPage)
admin.site.register(models.SeriesPage)
admin.site.register(models.Topic)
admin.site.register(models.TopicListPage)
