from __future__ import absolute_import, unicode_literals

import argparse
import getpass
import json

import MySQLdb
import requests
from bs4 import BeautifulSoup
from django.core.files.images import File, get_image_dimensions
from django.core.management.base import BaseCommand
from django.utils.six import BytesIO, text_type
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import Image

from articles.models import ArticlePage
from people.models import Contributor
from wordpress_importer.utils import get_setting

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


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
        self.image_download_domains = get_setting("IMAGE_DOWNLOAD_DOMAINS")

    def handle(self, **options):
        db_config = {
            'user': options.get('user', ''),
            'passwd': options.get('password', ''),
            'host': options.get('host', ''),
            'db': options.get('db', ''),
            'charset': 'utf8'
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
            elif meta_key == "userphoto_image_file":
                source = get_setting("USER_PHOTO_URL_PATTERN").format(
                    meta_value)
                filename = meta_value
                self.download_image(source, filename)
                contributor.headshot = Image.objects.get(title=filename)
            contributor.save()

    def get_post_data(self):
        cursor = self.connection.cursor()
        # TODO: get post time post_date_gmt
        # TODO: setup better filtering so that we get only the data that we
        # actually want to transfer.
        query = 'SELECT wp_posts.id, post_content, post_title, post_excerpt, post_name, user_email ' \
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
        # TODO: store a list of IDs for the posts that we are migrating.
        results = self.get_post_data()

        features_page = Page.objects.get(slug="features")
        # user = User.objects.all().first()

        for (post_id, post_content, post_title, post_excerpt, post_name,
             author_email) in results:
            pages = ArticlePage.objects.filter(slug=post_name)
            if pages.count() > 0:
                page = pages.first()
            else:
                page = ArticlePage(owner=None)
                features_page.add_child(instance=page)

            page.slug = post_name
            if post_title:
                page.title = post_title
            else:
                page.title = ''
            if post_content:
                updated_post_content = self.process_html_for_stream_field(
                    post_content)
                page.body = json.dumps(updated_post_content)
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

    def process_html_for_stream_field(self, html):
        processed_html = []
        html = self.process_html_for_images(html, use_image_names=True)
        parser = BeautifulSoup(html)

        for child in parser.body.children:
            processed_html.extend(self._process_element(child))

        return processed_html

    def _process_element(self, html):
        processed_element = []
        if html.name is None:
            processed_element.append({'type': 'Paragraph',
                                      'value': "<p>{}</p>".format(
                                          html.strip())})
        elif html.name == 'img':
            processed_element.append(self._process_image_tag(html))
        elif html.name == 'p' or html.name == 'div':

            children_contain_blocks = False
            indices_of_children_with_blocks = []
            all_children = list(html.children)
            for index, child in enumerate(all_children):
                if self._contains_stream_block(child):
                    indices_of_children_with_blocks.append(index)
                    children_contain_blocks = True

            if children_contain_blocks:
                processed_element.extend(self._process_container_element_children(indices_of_children_with_blocks, all_children))

            else:
                inner = html.decode_contents(formatter="html")
                if inner:
                    processed_element.append({'type': 'Paragraph',
                                              'value': "<p>{}</p>".format(
                                                  inner.strip())})

        return processed_element

    def _process_container_element_children(self, indices_of_children_with_blocks, all_children):
        processed_element = []
        last_index = 0
        for current_index in indices_of_children_with_blocks:
            child = "".join([text_type(x) for x in
                             all_children[last_index:current_index]])
            if child:
                processed_element.append({'type': 'Paragraph',
                                          'value': "<p>{}</p>".format(
                                              child.strip())})
            child = all_children[current_index]
            processed_element.extend((self._process_element(child)))
            last_index = current_index + 1

        child = "".join([text_type(x) for x in
                         all_children[last_index:len(all_children)]])
        if child:
            processed_element.append({'type': 'Paragraph',
                                      'value': "<p>{}</p>".format(
                                          child.strip())})

        return processed_element

    def _contains_stream_block(self, html):
        return html.name in ['div', 'p', 'img']

    def _process_image_tag(self, item):
        images = Image.objects.filter(title=item['src'])
        if images.first():
            return {'type': 'Image', 'value': images.first().id}
        else:
            return {'type': 'Paragraph',
                    'value': "<p>{}</p>".format(text_type(item))}

    def process_html_for_images(self, html, use_image_names=False):
        parser = BeautifulSoup(html)
        image_tags = parser.find_all('img')

        # TODO: check for existing image that is the same.  Maybe store the
        # original urls and only download if it has not been processed before.

        for image_tag in image_tags:
            source = image_tag['src']

            parsed_url = urlparse(source)
            if parsed_url.netloc in self.image_download_domains:

                filename = parsed_url.path.split("/")[-1]

                try:
                    updated_source_url = self.download_image(source, filename,
                                                             use_image_names)

                    html = html.replace(source, updated_source_url)
                except DownloadException:
                    pass
                    # TODO: maybe log something so we can look into it.

        return html

    def download_image(self, url, filename, use_image_names=False):
        response = requests.get(url)

        if response.status_code == 200:

            f = StringIO(response.content)

            dim = get_image_dimensions(f)  # (width, height)

            image = Image.objects.create(
                title=filename,
                uploaded_by_user=None,
                file=File(f, name=filename),
                width=dim[0],
                height=dim[1]
            )

            if use_image_names:
                updated_source_url = image.title
            else:
                updated_source_url = image.get_rendition(
                    'width-{}'.format(dim[0])).url
            return updated_source_url
        else:
            raise DownloadException()

    def load_indepth_posts(self):
        # links to other articles - class: idarticlecontainer
        pass


class DownloadException(Exception):
    pass
    # TODO: make this include useful information like the url and the response info
