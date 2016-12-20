import json
import os
from collections import OrderedDict

import unicodecsv as csv
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from articles.models import ArticlePage


class Command(BaseCommand):
    help = 'Update the relevant data for Twitterati members in all articles that serve an uploaded JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            'slug',
            help='The slug of the article you want to initialize or update'
        )

        parser.add_argument(
            'csvfile',
            help='Formatted CSV file to initialize the json data. See the docs.'
        )

    def handle(self, *args, **options):
        if not os.path.isfile(options['csvfile']):
            raise CommandError('Cannot find file {}.'.format(options['csvfile']))

        try:
            article = ArticlePage.objects.get(slug=options['slug'])
        except ArticlePage.DoesNotExist:
            raise CommandError('Cannot find article with slug {}.'.format(options['slug']))

        csv_file = open(options['csvfile'], 'rb')

        by_category = OrderedDict()
        rows = csv.reader(csv_file, encoding='utf-8')
        for row in rows:
            name, handle, bio, cat = row
            category = cat.split(' ', 1)[0].lower()
            if category not in by_category:
                by_category[category] = dict(
                    category = category,
                    description = cat.lower(),
                    members = [],
                )

            by_category[category]['members'].append(
                dict(
                    twitter_handle = handle,
                    profile_image_url = '',
                    full_name = name,
                    follower_count = '',
                    biography = bio,
                )
            )

        json_data = [by_category[key] for key in by_category]
        content_file = ContentFile(json.dumps(json_data, indent=4))

        article.json_file.save(
            '{}.json'.format(article.slug),
            content_file
        )
        self.stdout.write("Updated JSON file belonging to '{}'...".format(article))
