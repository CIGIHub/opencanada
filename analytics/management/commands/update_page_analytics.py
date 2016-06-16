from __future__ import absolute_import, division, unicode_literals

import datetime
import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now
from wagtail.contrib.wagtailfrontendcache.utils import (purge_page_from_cache,
                                                        purge_url_from_cache)
from wagtail.wagtailcore.models import Page

from analytics import utils
from core.models import HomePage


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
    help = 'Get the analytics data over the last week and update the articles in the system'

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--days',
            action='store',
            type=int,
            dest='days',
            default=7,
            help='The number of days to look back to determine popularity'
        )
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

        scopes = ['https://www.googleapis.com/auth/analytics.readonly']
        service_account_email = get_service_account_email()

        service = utils.get_service(
            'analytics',
            'v3',
            scopes,
            key_file_location,
            service_account_email
        )

        profile = utils.get_first_profile_id(service)

        days = options['days']
        start_time = now() - datetime.timedelta(days)
        start_date = start_time.strftime('%Y-%m-%d')

        data = service.data().ga().get(
            ids='ga:' + profile,
            start_date=start_date,
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
            pages = dict([(page.url, page) for page in Page.objects.live()])
            utils.reset_analytics(pages)
            for row in data['rows']:
                url, sessions = row
                if url not in pages:
                    continue

                page = pages[url]

                analytics = utils.get_analytics(page)
                analytics.last_period_views = sessions
                analytics.save()

        purge_url_from_cache(settings.BASE_URL + 'most-popular/')
        for page in HomePage.objects.live():
            purge_page_from_cache(page)
