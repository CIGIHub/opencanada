from __future__ import absolute_import, unicode_literals

from django.core.management.base import BaseCommand

from articles.models import (ArticlePage, ExternalArticlePage, Headline,
                             SeriesPage)


class Command(BaseCommand):
    description = 'Updates the default opacity value'

    def add_arguments(self, parser):
        parser.add_argument('original_opacity', type=int)
        parser.add_argument('new_opacity', type=int)

    def handle(self, **options):
        original_opacity = options.get('original_opacity', 30)
        new_opacity = options.get('new_opacity', 45)

        for page_type in [ArticlePage, ExternalArticlePage, SeriesPage]:
            for item in page_type.objects.filter(image_overlay_opacity=original_opacity):
                item.image_overlay_opacity = new_opacity
                revision = item.save_revision(
                    user=None,
                    submitted_for_moderation=False,
                )

                revision.publish()

        for item in Headline.objects.filter(image_overlay_opacity=original_opacity):
            item.image_overlay_opacity = new_opacity
            item.save()
