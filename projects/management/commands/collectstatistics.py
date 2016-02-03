from __future__ import unicode_literals

import argparse
import httplib2
from apiclient.discovery import build
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from oauth2client import client
from oauth2client import GOOGLE_REVOKE_URI
from oauth2client import GOOGLE_TOKEN_URI
from six.moves import xrange

from projects.models import ProjectPage


class Command(BaseCommand):
    help = 'Collect statistics on series and articles related to a project'

    def add_arguments(self, parser):
        # Postional arguments
        parser.add_argument('project',
                            type=str,
                            help='Title of the project containing the series and/or articles of interest')

        parser.add_argument('startdate',
                            type=self.valid_date,
                            help="Start date to use in analytics queries in the format of YYYY-MM-DD")

        parser.add_argument('enddate',
                            type=self.valid_date,
                            help="End date to use in analytics queries in the format of YYYY-MM-DD")

        # Named (optional) arguments
        parser.add_argument('--client-id',
                            default=settings.GOOGLE_DEVELOPER_CLIENT_ID,
                            dest='client_id',
                            help='OAuth 2.0 Client ID used to create credentials; required to authenticate before making API requests')

        parser.add_argument('--client-secret',
                            default=settings.GOOGLE_DEVELOPER_CLIENT_SECRET,
                            dest='client_secret',
                            help='OAuth 2.0 Client Secret used to create credentials; required to authenticate before making API requests')

        # NOTE: In order to obtain this, you must first grant permission to access the resource using the normal OAuth 2.0 flow;
        # you'll get both a short-lived access token that will expire and a refresh token that will not expire
        parser.add_argument('--refresh-token',
                            default=settings.GOOGLE_DEVELOPER_REFRESH_TOKEN,
                            dest='refresh_token',
                            help='OAuth 2.0 Refresh Token; required to authenticate before making API requests')

        parser.add_argument('--profile-id',
                            default=settings.GOOGLE_ANALYTICS_PROFILE_ID,
                            dest='profile_id',
                            help='Profile ID for viewing Google Analytics related to OpenCanada; required to request data')

        parser.add_argument('--metrics',
                            default='ga:pageviews,ga:uniquePageviews',
                            dest='metrics',
                            help='The aggregated statistics for user activity to your site, such as clicks or pageviews')

    def handle(self, *args, **options):
        # Get authentication tokens
        client_id = options['client_id']
        client_secret = options['client_secret']
        refresh_token = options['refresh_token']
        service = self._get_google_analytics_service_object(client_id, client_secret, refresh_token)

        # Get additional query string parameters
        profile_id = options['profile_id']
        metrics = options['metrics']

        # NOTE: If you don't know what profile ID you should use, you can figure it out using the service object
        # Step 1: Get the account; we use the first (and only) account here, but the logic is the same for multiple accounts
        # Look for an account with the following properties: {u'kind': u'analytics#account', u'name': u'www.opencanada.org'}
        accounts = service.management().accounts().list().execute()
        first_account_id = accounts['items'][0]['id']
        # Step 2: Get the web properties associated with the account
        # Look for a web property with the following properties: {u'kind': u'analytics#webproperty', u'name': u'www.opencanada.org'}
        web_properties = service.management().webproperties().list(accountId=first_account_id).execute()
        first_web_property_id = web_properties['items'][0]['id']
        # Step 3: Get the profiles associated with the account and web property of interest
        # Look for a profile with the following properties: {u'kind': u'analytics#profile', u'name': u'www.opencanada.org'}
        profiles = service.management().profiles().list(accountId=first_account_id,
                                                        webPropertyId=first_web_property_id).execute()
        first_profile_id = profiles['items'][0]['id']
        if profile_id != first_profile_id:
            self.stdout.write(self.style.WARNING("Specified profile ID '{}' does not match the expected value of '{}'; queries may fail.".format(profile_id, first_profile_id)))

        # Get data about the pages from DB first
        project_title = options['project']
        statistics = self._get_statistics_from_database(project_title)

        # Then update that with statistics from Google Analytics
        start_date = options['startdate']
        end_date = options['enddate']
        statistics = self._get_statistics_from_google_analytics(service, profile_id, start_date, end_date,
                                                                metrics, statistics)

        # Digest the results
        self._digest_statistics(statistics, metrics)

    def chunks(self, iterable, n):
        # Yield successive n-sized chunks from iterable
        for i in xrange(0, len(iterable), n):
            yield iterable[i:i + n]

    def valid_date(self, date_string):
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            message = "Not a valid date: '{0}'.".format(date_string)
            raise argparse.ArgumentTypeError(message)
        else:
            return date_string

    def _digest_statistics(self, statistics, metrics):
        metrics = metrics.split(',')
        line_values = ['title', 'pagePath', 'facebookLikes']
        line_values.extend(metrics)
        self.stdout.write(self.style.NOTICE(','.join(line_values)))
        for page_path in statistics:
            line_values = ['"{}"'.format(statistics[page_path]['title']),
                           page_path,
                           statistics[page_path]['facebook_likes']]
            for metric in metrics:
                if metric in statistics[page_path]:
                    line_values.append(statistics[page_path][metric])
                else:
                    line_values.append(0)
            self.stdout.write(self.style.NOTICE(','.join(['{}'.format(x) for x in line_values])))

    def _get_google_analytics_service_object(self, client_id, client_secret, refresh_token):
        # Validate authentication keys
        if not client_id:
            raise CommandError('Missing required setting: GOOGLE_DEVELOPER_CLIENT_ID')
        if not client_secret:
            raise CommandError('Missing required setting: GOOGLE_DEVELOPER_CLIENT_SECRET')
        if not refresh_token:
            raise CommandError('Missing required setting: GOOGLE_DEVELOPER_REFRESH_TOKEN')

        # Create credentials using refresh token
        credentials = client.OAuth2Credentials(None, client_id, client_secret, refresh_token, None, GOOGLE_TOKEN_URI,
                                               None, revoke_uri=GOOGLE_REVOKE_URI, id_token=None, token_response=None)

        # Create an httplib2.Http object and authorize it with our credentials
        http = httplib2.Http()
        http = credentials.authorize(http)

        # Build the Analytics Service Object with the authorized http object
        service = build('analytics', 'v3', http=http)
        return service

    def _get_statistics_from_database(self, project_title):
        statistics = {}
        project = ProjectPage.objects.get(title__iexact=project_title)
        pages = [x for x in project.project_articles()]
        pages.extend([x for x in project.project_series()])
        for page in pages:
            if page.url in statistics:
                self.stdout.write(self.style.ERROR("Already have a page with the URL '{}'!".format(page.url)))
            else:
                page_statistics = {
                    'title': page.title,
                    'facebook_likes': page.facebook_count,
                    'first_published_at': page.first_published_at.strftime('%Y-%m-%d')
                }
                statistics[page.url] = page_statistics
        return statistics

    def _get_statistics_from_google_analytics(self, service, profile_id, start_date, end_date, metrics, json_data):
        ids = 'ga:' + profile_id
        dimensions = 'ga:pagePath'
        data_rows = []

        # Batch the data in groups of 10 to limit querystring size
        for chunk in self.chunks(json_data.keys(), 10):
            filters = []
            for page_path in chunk:
                filters.append('ga:pagePath=={}'.format(page_path))
            filters = ','.join(filters)
            data_query = service.data().ga().get(ids=ids, start_date=start_date, end_date=end_date, metrics=metrics,
                                                 dimensions=dimensions, filters=filters)
            data = data_query.execute()
            data_rows.extend(data['rows'])

        # Update statistics
        metrics = metrics.split(',')
        for row in data_rows:
            page_path = row[0]
            additional_stats = {}
            for index, metric in enumerate(metrics):
                additional_stats[metric] = row[1 + index]
            json_data[page_path].update(additional_stats)

        return json_data
