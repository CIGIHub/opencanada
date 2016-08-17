from __future__ import unicode_literals

import argparse
import re
from datetime import datetime
from django.core.management.base import BaseCommand

from analytics import utils
from articles.models import ArticlePage, SeriesPage

class Command(BaseCommand):
    # usage = 'PYTHONIOENCODING=utf-8 python manage.py create_ga_report 2015-08-01 2016-08-01 > opencanadareport.tsv'
    help = 'Create a report containing Google Analytics for series and articles'

    def add_arguments(self, parser):
        # Postional arguments
        parser.add_argument('startdate',
                            type=self.valid_date,
                            help="Start date to use in analytics queries in the format of YYYY-MM-DD")

        parser.add_argument('enddate',
                            type=self.valid_date,
                            help="End date to use in analytics queries in the format of YYYY-MM-DD")

        # Optional arguments
        parser.add_argument('--dimensions',
                            default='ga:pagePath',
                            # default='ga:pagePath,ga:sourceMedium',
                            # default='ga:pagePath,ga:source,ga:medium',
                            dest='dimensions',
                            help='The data dimensions to use when querying for specified metrics, such as page path')

        parser.add_argument('--metrics',
                            default='ga:pageviews,ga:uniquePageviews,ga:avgTimeOnPage',
                            dest='metrics',
                            help='The aggregated statistics for user activity to your site, such as clicks or pageviews')

        # TODO: This doesn't actually make sense; the pivot logic is dependent on the other dimensions and the other
        # filters...maybe have an optional parameter that you specify like --pivot-dimension=source and then the logic
        # can be generalized to handle that...
        parser.add_argument('--other-dimensions',
                            default='ga:source',
                            dest='otherdimensions',
                            help='Other data dimensions to include when querying for specified metrics, such as page path')

        parser.add_argument('--other-filters',
                            default='ga:source=~.*facebook.com|twitter.com|(direct)|^google$',
                            dest='otherfilters',
                            help='Filters for the other data dimensions')

    def handle(self, *args, **options):
        # Build the service to communicate with the Google Analytics API
        scopes = ['https://www.googleapis.com/auth/analytics.readonly']
        key_file_location = utils.get_key_file_location()
        service_account_email = utils.get_service_account_email()
        service = utils.get_service(
            'analytics',
            'v3',
            scopes,
            key_file_location,
            service_account_email
        )

        # Get the profile to use with the service
        profile_id = utils.get_first_profile_id(service)

        # Get parameters
        start_date = options['startdate']
        end_date = options['enddate']
        dimensions = options['dimensions']
        metrics = options['metrics']
        other_dimensions = options['otherdimensions']
        other_filters = options['otherfilters']

        # Get data about the pages from database
        db_statistics_by_page_url = self._get_statistics_from_database(start_date, end_date)

        # Get data with statistics from Google Analytics
        ga_statistics, other_ga_stats = self._get_statistics_from_google_analytics(service, profile_id,
                                                                                   start_date, end_date,
                                                                                   dimensions, metrics,
                                                                                   other_dimensions, other_filters)

        # Merge the statistics from the different data sources and print them
        self._print_statistics(db_statistics_by_page_url, ga_statistics, other_ga_stats)

    def valid_date(self, date_string):
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            message = "Not a valid date: '{0}'.".format(date_string)
            raise argparse.ArgumentTypeError(message)
        else:
            return date_string

    def _print_statistics(self, db_statistics_by_page_url, ga_statistics_by_page_url, other_ga_stats_by_page_url):
        header_row = ['Title', 'URL', 'Published Date', 'Days Published', 'Parent Page', 'Category', 'Type',
                      'Word Count', 'Pageviews (PV)', 'Unique Pageviews (UPV)', 'Avg. Time on Page', 'facebook PV',
                      'facebook UPV', 'twitter PV', 'twitter UPV', 'direct PV', 'direct UPV', 'google PV', 'google UPV']
        print '\t'.join([x for x in header_row])
        for url in db_statistics_by_page_url.keys():
            page_data = db_statistics_by_page_url[url]
            data_row = self._format_page_data_for_output(page_data)
            ga_statistics = ga_statistics_by_page_url[url]
            assert len(ga_statistics) == 1
            other_statistics = other_ga_stats_by_page_url[url]
            data_row.extend(self._format_ga_data_for_output(ga_statistics[0], other_statistics))
            print '\t'.join([x for x in data_row])

    def _format_page_data_for_output(self, page_data):
        output = []
        output.append(page_data['title'])
        output.append(page_data['url'])
        published_date = page_data['published_date'].strftime('%Y-%m-%d')
        output.append(published_date)
        output.append(unicode(page_data['days_published']))
        output.append(page_data['parent_page'])
        output.append(page_data['category'])
        types = []
        if page_data['is_video']:
            types.append('Video')
        if page_data['is_interview']:
            types.append('Interview')
        if page_data['is_visualization']:
            types.append('Visualization')
        output.append(','.join(types))
        word_count = sum([x for x in page_data['word_count_by_type'].values()])
        output.append(unicode(word_count))
        return output

    def _format_ga_data_for_output(self, ga_statistics, other_statistics):
        # TODO: Here is the perfect example of why this Command isn't generic enough...
        output = [unicode(x) for x in ga_statistics]
        json_data = {
            'facebook': [0, 0],
            'twitter': [0, 0],
            'direct': [0, 0],
            'google': [0, 0]
        }
        for key in json_data.keys():
            filtered_stats = [x for x in other_statistics if key in x[0]]
            for stats in filtered_stats:
                json_data[key][0] += int(stats[1])
                json_data[key][1] += int(stats[2])
        output.extend(unicode(x) for x in json_data['facebook'])
        output.extend(unicode(x) for x in json_data['twitter'])
        output.extend(unicode(x) for x in json_data['direct'])
        output.extend(unicode(x) for x in json_data['google'])
        return output

    def _calculate_days_published(self, published_date, end_date):
        # TypeError: can't subtract offset-naive and offset-aware datetimes
        date_diff = end_date - published_date.replace(tzinfo=None)
        return date_diff.days

    # TODO: Investigate the possibility of simply extending all of our models/snippets/etc. with a Mixin that provides
    # a word_count function...
    def _calculate_word_count_by_type(self, page):
        types_to_ignore = [u'Embed', u'FullBleed', u'Image', u'Overflow', u'SectionBreak', u'Sharable']
        word_count_stats = {}
        # Generic 'body'...
        if page.body:
            for data in page.body.stream_data:
                type = data['type']
                if type in types_to_ignore:
                    continue
                if type not in word_count_stats:
                    word_count_stats[type] = 0
                value = data['value']
                try:
                    text = value['text']
                except KeyError:
                    word_count_stats[type] += 1
                    continue
                except TypeError:
                    text = value
                # 'List' type...
                if isinstance(text, list):
                    text = '\n'.join(text)
                words = self._get_words(text)
                word_count_stats[type] += len(words)
        # 'Chapters'...
        try:
            chapters = page.chapters
        except AttributeError:
            chapters = []
        if len(chapters) > 0:
            type = 'ChapterBody'
            text_keys = ['label', 'text']
            word_count_stats[type] = 0
            for chapter in page.chapters:
                # Recurse down the 'body' tree and collect all the 'text'...
                text = '\n'.join(self._get_body_text(chapter.value['body'], text_keys))
                words = self._get_words(text)
                word_count_stats[type] += len(words)
        return word_count_stats

    def _get_body_text(self, body, text_keys):
        texts = []
        for body_block in body:
            if isinstance(body_block.value, dict):
                if body_block.value.has_key('body'):
                    text = '\n'.join(self._get_body_text(body_block.value['body'], text_keys))
                else:
                    for key in text_keys:
                        if body_block.value.has_key(key):
                            try:
                                text = body_block.value[key].source
                            except AttributeError:
                                text = body_block.value[key]
                            except TypeError:
                                import pdb; pdb.set_trace()
                                i = 1
                    for key in body_block.value.keys():
                        if key not in ['body', 'expandable', 'heading_level', 'image', 'include_border', 'label', 'placement', 'text', 'use_dropcap']:
                            raise KeyError("'{}' not in the list of expected keys for a StreamField".format(key))
            elif isinstance(body_block.value, list):
                text = '\n'.join([x.source for x in body_block.value])
            else:
                try:
                    text = body_block.value.source
                except AttributeError:
                    text = body_block.value
            texts.append(text)
        return texts

    def _get_words(self, text):
        # Strip out MS-Word specific tags and other junk...probably don't have all of it, but this should handle most...
        pattern = '<o:DocumentProperties>.*</o:DocumentProperties>|\{mso.*;\}'
        text, replacements = re.subn(pattern, '', text, flags=re.DOTALL)
        # Strip HTML tags
        pattern = '<.*?>'
        text, replacements = re.subn(pattern, '', text, flags=re.DOTALL)
        words = re.findall(ur'\w+', text.replace(u'\xa0', ' ').encode('utf-8'))
        return words

    def _get_statistics_from_database(self, start_date, end_date):
        data_table = {}
        articles_of_interest = ArticlePage.objects.filter(first_published_at__range=['2015-08-01', '2016-08-01'])
        end_date_as_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        for article in articles_of_interest:
            data_row = {}
            data_row['title'] = article.title
            data_row['url'] = article.url
            data_row['published_date'] = article.first_published_at
            data_row['days_published'] = self._calculate_days_published(data_row['published_date'], end_date_as_datetime)
            data_row['parent_page'] = article.get_parent().title
            data_row['category'] = article.category.name
            data_row['is_video'] = article.video
            data_row['is_interview'] = article.interview
            data_row['is_visualization'] = article.visualization
            data_row['word_count_by_type'] = self._calculate_word_count_by_type(article)
            data_table[data_row['url']] = data_row

        series_of_interests = SeriesPage.objects.filter(first_published_at__range=['2015-08-01', '2016-08-01'])
        for series in series_of_interests:
            data_row = {}
            data_row['title'] = series.title
            data_row['url'] = series.url
            data_row['published_date'] = series.first_published_at
            data_row['days_published'] = self._calculate_days_published(data_row['published_date'], end_date_as_datetime)
            data_row['parent_page'] = series.get_parent().title
            data_row['category'] = ''
            data_row['is_video'] = False
            data_row['is_interview'] = False
            data_row['is_visualization'] = False
            data_row['word_count_by_type'] = self._calculate_word_count_by_type(series)
            data_table[data_row['url']] = data_row

        all_types = set([])
        for k, v in data_table.iteritems():
            word_count_stats = v['word_count_by_type']
            all_types.update(word_count_stats.keys())

        return data_table

    def _get_statistics_from_google_analytics(self, service, profile_id, start_date, end_date, dimensions, metrics,
                                              other_dimensions, other_filters):
        # Perform a query using the specified dimensions
        filters = [
            'ga:pagePath!~^/$',
            'ga:pagePath!~^/about',
            'ga:pagePath!~^/author/*',
            'ga:pagePath!~^/blog/*',
            'ga:pagePath!~^/contributors/*',
            'ga:pagePath!~^/event/*',
            'ga:pagePath!~^/search/*',
            'ga:pagePath!~^/tag/*',
            'ga:pagePath!~^/topics/*',
        ]
        filters = ';'.join(filters)
        base_data_dict = self._get_google_analytics_keyed_by_url(service, profile_id, start_date, end_date, dimensions,
                                                                 metrics, filters)

        # Perform another query with the addition of the other dimensions
        dimensions = ','.join([dimensions, other_dimensions])
        filters = ';'.join([filters, other_filters])
        other_data_dict = self._get_google_analytics_keyed_by_url(service, profile_id, start_date, end_date, dimensions,
                                                                  metrics, filters)

        return base_data_dict, other_data_dict

    def _get_google_analytics_keyed_by_url(self, service, profile_id, start_date, end_date, dimensions, metrics,
                                           filters, max_results=10000):
        ids = 'ga:' + profile_id

        # Perform a query using the specified dimensions, metrics, and filters
        data_rows = []
        start_index = 1
        while True:
            data_query = service.data().ga().get(ids=ids, start_date=start_date, end_date=end_date, metrics=metrics,
                                                 dimensions=dimensions, filters=filters, start_index=start_index,
                                                 max_results=max_results)
            data = data_query.execute()
            data_rows.extend(data['rows'])
            total_rows = int(data['totalResults'])
            start_index += max_results
            if len(data_rows) >= total_rows:
                break

        data_dict = {}
        for row in data_rows:
            url = row[0]
            if not data_dict.has_key(url):
                data_dict[url] = []
            data_dict[url].append(row[1:])

        return data_dict
