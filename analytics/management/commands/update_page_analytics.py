from __future__ import absolute_import, division, unicode_literals

import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.wagtailcore.models import Page

from analytics import utils


def get_creds_path():
    message = 'Setting ANALYTICS_CREDS_PATH must be defined, exist and be a directory.'
    try:
        path = getattr(settings, 'ANALYTICS_CREDS_PATH')
    except AttributeError:
        raise ImproperlyConfigured(message)

    if not os.path.isdir(path):
        raise ImproperlyConfigured(message)

    return path


def get_service_account_email():
    message = 'Setting ANALYTICS_SERVICE_ACCOUNT_EMAIL must be defined and non empty'
    try:
        email = getattr(settings, 'ANALYTICS_SERVICE_ACCOUNT_EMAIL')
    except AttributeError:
        raise ImproperlyConfigured(message)

    if email is None or email == '':
        raise ImproperlyConfigured(message)

    return email


class Command(BaseCommand):
    help = 'Get the analytics data over the last week and update the articles in te system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Output the analytics but do not update the database'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        creds_path = get_creds_path()

        key_file_location = os.path.join(creds_path, 'open-canada-analytics.p12')

        if not os.path.isfile(key_file_location):
            raise ImproperlyConfigured(
                '{} must be a file which contains your api key.'.format(key_file_location)
            )

        scope = ['https://www.googleapis.com/auth/analytics.readonly']
        service_account_email = get_service_account_email()

        service = utils.get_service(
            'analytics',
            'v3',
            scope,
            key_file_location,
            service_account_email
        )

        profile = utils.get_first_profile_id(service)

        data = service.data().ga().get(
            ids='ga:' + profile,
            start_date='7daysAgo',
            end_date='today',
            dimensions='ga:pagePath',
            metrics='ga:sessions',
            sort='-ga:sessions',
            filters='ga:sessions>=1',
        ).execute()

        if dry_run:
            for row in data['rows']:
                url, session = row
                print('{}: {}'.format(url, session))
            sys.exit(0)

        with transaction.atomic():
            # TODO should I filter on liveness?
            pages = dict([(page.url, page) for page in Page.objects.live()])
            utils.reset_analytics(pages)
            for row in data['rows']:
                url, sessions = row
                if url not in pages:
                    continue

                page = pages[url]

                analytics = utils.get_analytics(page)
                analytics.last_week_views = sessions
                analytics.save()

        # TODO Cache: we need to invalid the cache for any page which is effected
        # by the analytics such as the home page
        # http://docs.wagtail.io/en/v1.0/reference/contrib/frontendcache.html#invalidating-index-pages
