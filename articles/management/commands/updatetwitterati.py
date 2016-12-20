import json
import math
import os
from io import BytesIO

import requests
import tweepy
from django.conf import settings
from django.core.files.base import ContentFile, File
from django.core.management.base import BaseCommand, CommandError
from six.moves.urllib.parse import urlparse

from articles.models import ArticlePage


class Command(BaseCommand):
    help = 'Update the relevant data for Twitterati members in all articles that serve an uploaded JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            'slug',
            help='The slug of the article you want to initialize or update'
        )

        parser.add_argument('--consumerkey',
                            default=settings.TWITTER_API_CONSUMER_KEY,
                            dest='consumer_key',
                            help='Twitter API Consumer Key; required to authenticate before making API requests')

        parser.add_argument('--consumersecret',
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
        try:
            article = ArticlePage.objects.get(slug=options['slug'])
        except ArticlePage.DoesNotExist:
            raise CommandError('Cannot find article with slug {}.'.format(options['slug']))

        # Get authentication tokens
        consumer_key = options['consumer_key']
        consumer_secret = options['consumer_secret']
        access_token = options['access_token']
        access_token_secret = options['access_token_secret']
        twitter_api = self._get_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret)

        json_file = article.json_file
        json_data = json.load(article.json_file)
        try:
            updated_json_data = self._get_updated_twitterati_data(
                json_data,
                twitter_api,
                article
            )

            updated_json_data = self._cache_twitterati_images(json_data, article.theme, json_file.storage)

            pre_save_name = json_file.name
            json_file.save(pre_save_name, ContentFile(json.dumps(updated_json_data, indent=4)))

            self.stdout.write(self.style.NOTICE("Updated JSON file belonging to '{}'...".format(article)))
        except (tweepy.TweepError, ValueError) as e:
            # Ignore exceptions and continue
            self.stdout.write(self.style.WARNING('{}({})'.format(type(e).__name__, e)))

    def _format_followers_count(self, count):
        # It's ok to re-format the count as a float with .0f since you can't have partial followers no rounding will occur
        format_strings = ['{:.0f}{}', '{:.2f}{}', '{:.2f}{}', '{:.2f}{}', '{:.2f}{}']
        milli_codes = ['', 'K', 'M', 'B', 'T']
        assert len(format_strings) == len(milli_codes)
        count_as_float = float(count)
        milli_index = max(0, min(len(milli_codes) - 1, int(math.floor(math.log10(abs(count_as_float)) / 3))))
        return format_strings[milli_index].format(count_as_float / 10 ** (3 * milli_index), milli_codes[milli_index])

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
        for category in json_data:
            members = category['members']
            twitter_handles = [member['twitter_handle'] for member in members]

            users = twitter_api.lookup_users(screen_names=twitter_handles)

            twitterati_updates = {}
            for user in users:
                formatted_follower_count = self._format_followers_count(user.followers_count)
                twitterati_updates[user.screen_name.lower()] = {
                    'profile_image_url': user.profile_image_url.replace('_normal', ''),
                    'follower_count': formatted_follower_count
                }

            for member in members:
                key = member['twitter_handle'].lower()
                updates = twitterati_updates.get(key)
                if updates:
                    member.update(updates)
                else:
                    self.stdout.write(self.style.WARNING("Mismatched screen name? {}".format(key)))

        return json_data

    def _cache_twitterati_images(self, json_data, context, storage):
        try:
            folder = context.folder
            storage.exists(folder)
        except AttributeError:
            self.stdout.write(self.style.WARNING("Cannot determine where images should be cached from context '{}'!".format(context)))
            return json_data

        # Go back over members and upload the image to storage
        for category in json_data:
            members = category['members']
            for member in members:
                image_url = member['profile_image_url']
                url_parts = urlparse(image_url)
                path_parts = os.path.split(url_parts.path)
                filename = path_parts[-1]
                relative_path = os.path.join(folder, 'img', filename)
                if not storage.exists(relative_path):
                    self.stdout.write(self.style.NOTICE("Attempting to download image file '{}'...".format(relative_path)))
                    response = requests.get(image_url, stream=True)
                    if response.status_code == 200:
                        buffer = BytesIO()
                        for chunk in response:
                            buffer.write(chunk)
                        fp = File(buffer, filename)
                        storage.save(relative_path, fp)
                        # Only update the image_url if we successfully saved the file to storage
                        new_image_url = relative_path
                        self.stdout.write(self.style.NOTICE("Image file downloaded to '{}'...".format(relative_path)))
                    else:
                        # Could not retrieve file from URL, so do not change it
                        new_image_url = image_url
                        self.stdout.write(self.style.WARNING("Could not download image file '{}'!".format(relative_path)))
                else:
                    # File is already there, so change the URL to reference it
                    new_image_url = relative_path
                    self.stdout.write(self.style.NOTICE("Image file '{}' already exists...".format(relative_path)))
                member['profile_image_url'] = new_image_url

        return json_data
