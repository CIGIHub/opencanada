from __future__ import absolute_import, unicode_literals

from datetime import datetime

from django.core.management.base import BaseCommand
from wagtail.wagtailcore.models import Page


class Command(BaseCommand):
    description = 'Updates the publish dates for pages'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)
        parser.add_argument('date', type=datetime)

    def handle(self, **options):
        page_id = options.get('id', -1)
        new_date = options.get('date', None)

        if page_id > 0 and new_date:
            page = Page.objects.get(id=page_id)

            page.first_published_at = new_date

            revision = page.save_revision(
                user=None,
                submitted_for_moderation=False,
            )

            revision.publish()
