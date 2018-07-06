from __future__ import absolute_import, division, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Analytics(models.Model):
    page = models.OneToOneField('wagtailcore.Page', on_delete=models.CASCADE)
    last_period_views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'analytics'

    def __str__(self):
        return "Analytics for {}".format(self.page.title)
