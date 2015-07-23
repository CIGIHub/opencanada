from django.contrib import admin

from . import models

admin.site.register(models.NewsletterPage)
admin.site.register(models.NewsletterArticleLink)
admin.site.register(models.ExternalArticle)
admin.site.register(models.NewsletterExternalArticleLink)
admin.site.register(models.Source)
admin.site.register(models.ExternalSourceLink)
admin.site.register(models.Event)
admin.site.register(models.NewsletterEventLink)
admin.site.register(models.Organization)
admin.site.register(models.EventOrganizationLink)
