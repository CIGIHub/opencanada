import json
import math
import tweepy

from operator import itemgetter

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Update the relevant data for Twitterati members in the specified JSON file'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('path_to_json', type=str)

    def handle(self, *args, **options):
        '''
        Possible self.style values:
        ['ERROR', 'ERROR_OUTPUT',
        'HTTP_BAD_REQUEST', 'HTTP_INFO', 'HTTP_NOT_FOUND', 'HTTP_NOT_MODIFIED', 'HTTP_REDIRECT', 'HTTP_SERVER_ERROR', 'HTTP_SUCCESS',
        'MIGRATE_FAILURE', 'MIGRATE_HEADING', 'MIGRATE_LABEL', 'MIGRATE_SUCCESS',
        'NOTICE',
        'SQL_COLTYPE', 'SQL_FIELD', 'SQL_KEYWORD', 'SQL_TABLE',
        'WARNING']
        '''
        with open(options['path_to_json'], 'r') as jsonfile:
            data = json.load(jsonfile)
        consumer_key = '<consumer_key>'
        consumer_secret = '<consumer_secret>'
        access_token = '<access_token>'
        access_token_secret = '<access_token_secret>'
        twitter_api = self._get_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret)
        new_data = self._update_twitterati(data, twitter_api)
        import pdb; pdb.set_trace()
        with open(options['path_to_json'], 'w') as jsonfile:
            json.dump(new_data, jsonfile, indent=4)

    def _format_followers_count(self, count):
        milli_codes = ['','K','M','B','T']
        count_as_float = float(count)
        milli_index = max(0,min(len(milli_codes)-1, int(math.floor(math.log10(abs(count_as_float))/3))))
        return '{:.2f}{}'.format(count_as_float/10**(3*milli_index), milli_codes[milli_index])

    def _get_twitter_api(self, consumer_key, consumer_secret, access_token, access_token_secret):
        # Authenticate
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Construct the API instance
        api = tweepy.API(auth)
        return api

    def _update_twitterati(self, json_data, twitter_api):
        # Collect all screen names (twitter handles)
        twitter_handles = []
        for category in json_data:
            members = category['members']
            twitter_handles.extend([member['twitter_handle'] for member in members])
        for twitter_handle in twitter_handles:
            self.stdout.write(self.style.NOTICE(twitter_handle))

        # API lookup for all users
        users = twitter_api.lookup_users(screen_names=twitter_handles)

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
