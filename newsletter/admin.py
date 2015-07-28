from django.contrib import admin

from . import models

admin.site.register(models.NewsletterPage)
admin.site.register(models.NewsletterArticleLink)
admin.site.register(models.NewsletterExternalArticleLink)
