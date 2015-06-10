from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class PostImports(models.Model):
    post_id = models.IntegerField()

    def __str__(self):
        return "%d" % self.post_id


@python_2_unicode_compatible
class ImageImports(models.Model):
    original_url = models.CharField(max_length=1024)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
