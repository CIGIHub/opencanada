import json
import math
import tweepy

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from articles.models import ArticlePage


class Command(BaseCommand):
    help = 'Update the relevant data for Twitterati members in all articles that serve an uploaded JSON file'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--files',
            dest='json_files',
            nargs='+',
            help='Update the relevant data for Twitterati members in the specified JSON file(s)')

        parser.add_argument('--key',
            default=settings.TWITTER_API_CONSUMER_KEY,
            dest='consumer_key',
            help='Twitter API Consumer Key; required to authenticate before making API requests')

        parser.add_argument('--secret',
            default=settings.TWITTER_API_CONSUMER_SECRET,
            dest='consumer_secret',
            help='Twitter API Consumer Secret; required to authenticate before making API requests')

        parser.add_argument('--token',
            default=settings.TWITTER_API_ACCESS_TOKEN,
            dest='access_token',
            help='Twitter API Access Token; required to authenticate before making API requests')

        parser.add_argument('--token-secret',
            default=settings.TWITTER_API_ACCESS_TOKEN_SECRET,
            dest='access_token_secret',
            help='Twitter API Access Token Secret; required to authenticate before making API requests')

    def handle(self, *args, **options):
        # Get authentication tokens
        consumer_key = options['consumer_key']
        consumer_secret = options['consumer_secret']
        access_token = options['access_token']
        access_token_secret = options['access_token_secret']
        twitter_api = self._get_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret)

        if not options['json_files'] is None:
            raise NotImplementedError('Not implemented yet...')
        else:
            matching_articles = ArticlePage.objects.exclude(json_file__isnull=True).exclude(json_file__exact='')
            for article in matching_articles:
                json_file = article.json_file
                json_data = json.load(article.json_file)
                try:
                    updated_json_data = self._get_updated_twitterati_data(json_data, twitter_api, article)
                    pre_save_name = json_file.name
                    # Remove previous file since we will replace it with an updated one
                    json_file.storage.delete(pre_save_name)
                    # Save the new contents to a file with the same name as the one uploaded to the article
                    json_file.save(pre_save_name, ContentFile(json.dumps(updated_json_data, indent=4)))
                    self.stdout.write(self.style.NOTICE("Updated JSON file belonging to '{}'...".format(article)))
                except (tweepy.TweepError, ValueError) as e:
                    # Ignore exceptions and continue
                    self.stdout.write(self.style.WARNING('{}({})'.format(type(e).__name__, e)))

    def _format_followers_count(self, count):
        milli_codes = ['','K','M','B','T']
        count_as_float = float(count)
        milli_index = max(0, min(len(milli_codes) - 1, int(math.floor(math.log10(abs(count_as_float)) / 3))))
        return '{:.2f}{}'.format(count_as_float/10**(3*milli_index), milli_codes[milli_index])

    def _get_twitter_api(self, consumer_key, consumer_secret, access_token, access_token_secret):
        # Validate authentication keys
        if not consumer_key:
            raise CommandError('Missing required setting: TWITTER_API_CONSUMER_KEY')
        if not consumer_secret:
            raise CommandError('Missing required setting: TWITTER_API_CONSUMER_SECRET')
        if not access_token:
            raise CommandError('Missing required setting: TWITTER_API_ACCESS_TOKEN')
        if not access_token_secret:
            raise CommandError('Missing required setting: TWITTER_API_ACCESS_TOKEN_SECRET')

        # Authenticate
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Construct the API instance
        api = tweepy.API(auth)
        return api

    def _get_updated_twitterati_data(self, json_data, twitter_api, context):
        # Collect all screen names (twitter handles)
        twitter_handles = []
        try:
            for category in json_data:
                members = category['members']
                twitter_handles.extend([member['twitter_handle'] for member in members])
        except:
            # JSON objects do not correspond to the expected model for Twitterati members
            raise ValueError('Could not parse JSON into expected structure for Twitterati members')

        self.stdout.write(self.style.NOTICE("Found {} Twitterati member(s) in '{}'...".format(len(twitter_handles), context)))

        try:
            # API lookup for all users
            users = twitter_api.lookup_users(screen_names=twitter_handles)
        except tweepy.TweepError as e:
            raise e

        # Extract necessary fields and key them by screen name
        twitterati_updates = {}
        for user in users:
            formatted_follower_count = self._format_followers_count(user.followers_count)
            twitterati_updates[user.screen_name.lower()] = {
                'profile_image_url' : user.profile_image_url.replace('_normal', ''),
                'follower_count' : formatted_follower_count
            }

        # Go back over members and update data
        for category in json_data:
            members = category['members']
            for member in members:
                key = member['twitter_handle'].lower()
                updates = twitterati_updates[key]
                member.update(updates)

        return json_data
