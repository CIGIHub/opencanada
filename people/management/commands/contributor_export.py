from __future__ import unicode_literals

import json

from django.core.management.base import BaseCommand

from people.models import ContributorPage


class Command(BaseCommand):
    help = 'Exports information about contributors to standard output.'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)

    def handle(self, *args, **options):
        # Filter: only contributor which have published in a given year.
        contributors = ContributorPage.objects.filter(
            article_links__article__first_published_at__year=options['year']
        ).distinct().order_by('last_name')

        data = [
            dict(full_name=contributor.full_name, contributor_url=contributor.url)
            for contributor in contributors
        ]

        string_output = json.dumps(data, indent=4)
        self.stdout.write(string_output)
