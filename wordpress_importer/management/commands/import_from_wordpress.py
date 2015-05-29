from __future__ import absolute_import, unicode_literals

import argparse
import getpass

import MySQLdb
from django.core.management.base import BaseCommand
from wagtail.wagtailcore.models import Page

from core.models import LegacyArticlePage
from people.models import Contributor


class PasswordPromptAction(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest=None,
                 nargs=0,
                 default=None,
                 required=False,
                 type=None,
                 metavar=None,
                 help=None):
        super(PasswordPromptAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            default=default,
            required=required,
            metavar=metavar,
            type=type,
            help=help)

    def __call__(self, parser, args, values, option_string=None):
        password = getpass.getpass()
        setattr(args, self.dest, password)


class Command(BaseCommand):
    description = 'Imports data from existing wordpress site'

    def add_arguments(self, parser):
        parser.add_argument('host', type=str)
        parser.add_argument('db', type=str)
        parser.add_argument('user', type=str)
        parser.add_argument('password', action=PasswordPromptAction)

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.connection = None

    def handle(self, **options):
        db_config = {
            'user': options.get('user', ''),
            'passwd': options.get('password', ''),
            'host': options.get('host', ''),
            'db': options.get('db', ''),
        }
        self.open_connection(db_config)
        self.load_contributors()
        self.load_posts()
        self.close_connection()

    def open_connection(self, database_configuration):
        self.connection = MySQLdb.connect(**database_configuration)

    def close_connection(self):
        self.connection.close()

    def get_contributor_data(self):
        cursor = self.connection.cursor()

        # TODO: twitter handle not coming through in this data.
        # TODO: where is the long bio?
        # TODO: get the images.
        query = 'SELECT user_email, meta_key, meta_value FROM wp_users ' \
                'inner join `wp_usermeta` ' \
                'on id=user_id ' \
                'WHERE ID IN ' \
                '(SELECT ID FROM `wp_users` ' \
                'inner join `wp_usermeta` ' \
                'on id=user_id ' \
                'where meta_value like "%contributor%"' \
                ') AND meta_key in ("first_name", "last_name", "nickname", "twitter", "description", "userphoto_image_file")'

        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def load_contributors(self):
        results = self.get_contributor_data()

        for (user_email, meta_key, meta_value) in results:
            contributor, created = Contributor.objects.get_or_create(
                email=user_email)
            if meta_key == "first_name":
                contributor.first_name = meta_value
            elif meta_key == "last_name":
                contributor.last_name = meta_value
            elif meta_key == "nickname":
                contributor.nickname = meta_value
            elif meta_key == "twitter":
                contributor.twitter_handle = meta_value
            elif meta_key == "description":
                contributor.short_bio = meta_value
            contributor.save()

    def get_post_data(self):
        cursor = self.connection.cursor()
        # post_author, post_date_gmt,
        query = 'SELECT post_content, post_title, post_excerpt, post_name, user_email ' \
                'FROM wp_posts INNER JOIN wp_users ' \
                'ON wp_posts.post_author = wp_users.ID ' \
                'WHERE wp_posts.ID in ' \
                '(SELECT wp_posts.ID FROM `wp_term_relationships` ' \
                'inner join `wp_posts` ' \
                'on object_id=wp_posts.ID ' \
                'inner join wp_term_taxonomy ' \
                'on wp_term_taxonomy.term_taxonomy_id=wp_term_relationships.term_taxonomy_id ' \
                'inner join wp_terms ' \
                'on wp_term_taxonomy.term_id=wp_terms.term_id ' \
                'where taxonomy="category" ' \
                'and post_status = "publish" and wp_terms.name="Features")'

        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def load_posts(self):
        results = self.get_post_data()

        features_page = Page.objects.get(slug="features")
        # user = User.objects.all().first()

        for (post_content, post_title, post_excerpt, post_name,
             author_email) in results:
            pages = LegacyArticlePage.objects.filter(slug=post_name)
            if pages.count() > 0:
                page = pages.first()
            else:
                page = LegacyArticlePage(owner=None)
                features_page.add_child(instance=page)

            page.slug = post_name
            if post_title:
                page.title = post_title
            else:
                page.title = ''
            if post_content:
                page.body = post_content
            else:
                page.body = ''
            if post_excerpt:
                page.excerpt = post_excerpt
            else:
                page.excerpt = ''

            contributors = Contributor.objects.filter(email=author_email)
            page.author = contributors.first()

            revision = page.save_revision(
                user=None,
                submitted_for_moderation=False,
            )
            revision.publish()
