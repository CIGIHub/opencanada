from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from wagtail.snippets.models import register_snippet


@python_2_unicode_compatible
class Interactive(models.Model):
    name = models.TextField()
    template = models.TextField()

    def __str__(self):
        return self.name

register_snippet(Interactive)
