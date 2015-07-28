from __future__ import absolute_import, unicode_literals

import argparse
import getpass
import json
import re

import requests
from bs4 import BeautifulSoup, Comment, element
from django.core.files.images import File, get_image_dimensions
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.six import BytesIO, text_type
from django.utils.text import slugify
from wagtail.wagtailcore.models import Page

import MySQLdb
from articles.models import (ArticleAuthorLink, ArticleCategory, ArticlePage,
                             ArticleTopicLink, SeriesArticleLink, SeriesPage,
                             Topic)
from images.models import AttributedImage
from people.models import ContributorListPage, ContributorPage
from wordpress_importer.models import (ImageImport, ImportDownloadError,
                                       PostImport, TagImport)
from wordpress_importer.utils import get_setting

try:
    from urlparse import urlparse
    from urlparse import unquote
except ImportError:
    from urllib.parse import urlparse
    from urllib.parse import unquote


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
        self.category_names_to_id = None
        self.category_id_to_slug = None

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
        self.load_series_posts()
        self.close_connection()

    def open_connection(self, database_configuration):
        self.connection = MySQLdb.connect(**database_configuration)

    def close_connection(self):
        self.connection.close()

    def get_category_slug(self, name):
        if not self.category_names_to_id:
            self.category_names_to_id = {}
            self.category_id_to_slug = {}
            self.build_category_dictionary()

        category_id = self.category_names_to_id[name]
        return self.category_id_to_slug[category_id]

    def get_contributor_data(self):
        cursor = self.connection.cursor()

        query = 'SELECT user_email, meta_key, meta_value FROM wp_users ' \
                'inner join wp_usermeta ' \
                'on id=user_id ' \
                'WHERE ID IN ' \
                '(SELECT ID FROM wp_users ' \
                'inner join wp_usermeta ' \
                'on id=user_id ' \
                'where meta_value like "%contributor%"' \
                ') AND meta_key in ("first_name", "last_name", "nickname", ' \
                '"twitter", "description", "userphoto_image_file") ' \
                'AND meta_value != ""'

        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        cursor = self.connection.cursor()
        query = 'SELECT user_email, fields.name, data.value FROM wp_users ' \
                'inner join wp_cimy_uef_data as data ' \
                'on wp_users.id = data.user_id ' \
                'inner join wp_cimy_uef_fields as fields ' \
                'on fields.id = data.field_id ' \
                'WHERE fields.name IN ("TWITTER", "SHORT_BIO") ' \
                'AND data.value != ""'

        cursor.execute(query)
        extra_results = cursor.fetchall()
        cursor.close()
        results += extra_results

        return results

    def load_contributors(self):
        results = self.get_contributor_data()

        contributor_list_page = ContributorListPage.objects.get(slug="contributors")

        for (user_email, meta_key, meta_value) in results:

            pages = ContributorPage.objects.filter(email=user_email)
            if pages.count() > 0:
                page = pages.first()
            else:
                page = ContributorPage(owner=None)
                contributor_list_page.add_child(instance=page)

            page.email = user_email\

            if meta_key == "first_name":
                page.first_name = meta_value
            elif meta_key == "last_name":
                page.last_name = meta_value
            elif meta_key == "nickname":
                page.nickname = meta_value
            elif meta_key == "twitter" or meta_key == "TWITTER":
                if meta_value.find("/") > 0:
                    meta_value = meta_value.split("/")[-1]
                if not meta_value.startswith("@"):
                    meta_value = "@{}".format(meta_value)
                page.twitter_handle = meta_value
            elif meta_key == "SHORT_BIO":
                page.short_bio = meta_value
            elif meta_key == "description":
                page.long_bio = meta_value
            # elif meta_key == "userphoto_image_file":
            #     source = get_setting("USER_PHOTO_URL_PATTERN").format(
            #         meta_value)
            #     filename = meta_value
                # try:
                #     self.download_image(source, filename)
                #     page.headshot = AttributedImage.objects.get(title=filename)
                # except DownloadException as e:
                #     if e.response:
                #         ImportDownloadError.objects.create(url=e.url, status_code=e.response.status_code)
                #     else:
                #         ImportDownloadError.objects.create(url=e.url, status_code=404)

            revision = page.save_revision(
                user=None,
                submitted_for_moderation=False,
            )
            revision.publish()

    def get_category_data(self):
        query = 'SELECT wp_terms.name, wp_terms.term_id, wp_terms.slug, parent ' \
                'FROM wp_term_taxonomy ' \
                'INNER JOIN wp_terms ON wp_term_taxonomy.term_id = wp_terms.term_id ' \
                'WHERE taxonomy="category"' \
                'ORDER BY parent'

        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def build_category_dictionary(self):
        results = self.get_category_data()

        for name, term_id, slug, parent_id in results:
            self.category_names_to_id[name] = term_id
            if parent_id == 0:
                self.category_id_to_slug[term_id] = slug
            else:
                full_slug = "/".join([self.category_id_to_slug[parent_id], slug])
                self.category_id_to_slug[term_id] = full_slug

    def get_post_query(self, post_type):
        query = 'SELECT DISTINCT wp_posts.id, post_content, post_title, ' \
                'post_excerpt, post_name, user_email, post_date_gmt ' \
                'FROM wp_posts INNER JOIN wp_users ' \
                'ON wp_posts.post_author = wp_users.ID ' \
                'WHERE wp_posts.ID in ' \
                '(SELECT wp_posts.ID FROM wp_term_relationships ' \
                'inner join wp_posts ' \
                'on object_id=wp_posts.ID ' \
                'inner join wp_term_taxonomy ' \
                'on wp_term_taxonomy.term_taxonomy_id=wp_term_relationships.term_taxonomy_id ' \
                'inner join wp_terms ' \
                'on wp_term_taxonomy.term_id=wp_terms.term_id ' \
                'where taxonomy="category" ' \
                'and post_status = "publish" and wp_terms.name="{}")'

        query = query.format(post_type)

        if post_type == "Features":
            query = "{} {}".format(
                query,
                """
                and wp_posts.ID not in
                (SELECT wp_posts.ID FROM `wp_term_relationships`
                inner join `wp_posts`
                on object_id=wp_posts.ID
                inner join wp_term_taxonomy
                on wp_term_taxonomy.term_taxonomy_id=wp_term_relationships.term_taxonomy_id
                inner join wp_terms
                on wp_term_taxonomy.term_id=wp_terms.term_id
                where taxonomy="category"
                and post_status = "publish" and (wp_terms.name="Dispatch"
                or wp_terms.name="Roundtable"
                or wp_terms.name="Blogs"
                or wp_terms.name = 'The Think Tank'
                or wp_terms.name = 'National Capital Branch News'
                or wp_terms.name = 'Readings'
                or wp_terms.name = 'CIC in the News'
                or wp_terms.name = 'Op-eds'
                or wp_terms.name = 'Reports'
                or wp_terms.name = 'Open Watch'
                or wp_terms.name = 'Visualizations'))"""
            )

        return query

    def get_post_data(self, post_type):
        cursor = self.connection.cursor()
        query = self.get_post_query(post_type)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_post_image_data(self, post_id):
        cursor = self.connection.cursor()
        query = "SELECT guid " \
                "FROM wp_posts " \
                "WHERE ID in " \
                "(SELECT meta_value " \
                "FROM wp_postmeta " \
                "WHERE post_id='{}' " \
                "AND meta_key='_thumbnail_id')".format(post_id)
        cursor.execute(query)
        results = cursor.fetchone()
        cursor.close()

        if results:
            return results[0]
        else:
            return None

    def get_download_path_and_filename(self, original_url, url_pattern, images_folder="uploads"):
        parsed_url = urlparse(original_url)
        path_parts = parsed_url.path.split("/")
        uploads_index = path_parts.index(images_folder)
        partial_path = "/".join(path_parts[uploads_index + 1:])
        filename = "_".join(path_parts[uploads_index + 1:])

        source = url_pattern.format(partial_path)

        return source, filename

    def update_post_image_data(self, post, post_id):
        results = self.get_post_image_data(post_id)
        if results:
            original_photo_url = results

            source, filename = self.get_download_path_and_filename(
                original_photo_url,
                text_type(get_setting("ARTICLE_PHOTO_URL_PATTERN"))
            )
            try:
                self.download_image(source, filename)
                post.main_image = AttributedImage.objects.get(title=filename)
            except DownloadException as e:
                if e.response:
                    ImportDownloadError.objects.create(url=e.url, status_code=e.response.status_code)
                else:
                    ImportDownloadError.objects.create(url=e.url, status_code=404)

    def get_category_type(self, name):
        if name == "101s":
            return "explainer"
        elif name == "Roundtable":
            return "roundtable-blog-post"
        elif name == "Dispatch":
            return "dispatch-blog-post"
        elif name == "Comments":
            return "commentary"
        elif name == "Essays":
            return "essay"
        elif name == "Graphics" or name == "Visualizations":
            return "infographic"
        elif name == "Interviews":
            return "interview"
        elif name == "Rapid Response Group":
            return "rapid-response"
        elif name == "In Depth":
            return "series"
        else:
            return "feature"

    def load_posts(self):
        for post_type in ["Features", "101s", "Roundtable",
                          "Dispatch", "Comments", "Essays",
                          "Graphics", "Visualizations", "Interviews", "Rapid Response Group"]:

            results = self.get_post_data(post_type)

            features_page = Page.objects.get(slug="features")
            feature_category = ArticleCategory.objects.get(slug=self.get_category_type(post_type))

            for (post_id, post_content, post_title, post_excerpt, post_name,
                 author_email, post_date) in results:

                cleaned_post_name = unquote(post_name).encode('ascii', 'ignore')

                pages = ArticlePage.objects.filter(slug=cleaned_post_name)
                if pages.count() > 0:
                    page = pages.first()
                else:
                    page = ArticlePage(owner=None, category=feature_category)
                    features_page.add_child(instance=page)

                if not page.main_image:
                    self.update_post_image_data(page, post_id)

                page.slug = cleaned_post_name

                if post_title:
                    page.title = post_title
                else:
                    page.title = ''
                if post_date:
                    page.first_published_at = timezone.make_aware(post_date, timezone.pytz.timezone('GMT'))
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

                contributor = ContributorPage.objects.filter(email=author_email).first()
                if contributor:
                    author_link, created = ArticleAuthorLink.objects.get_or_create(
                        author=contributor,
                        article=page
                    )
                    author_link.save()

                revision = page.save_revision(
                    user=None,
                    submitted_for_moderation=False,
                )
                revision.publish()

                original_permalink = "/".join([self.get_category_slug(post_type), post_name])

                import_record, created = PostImport.objects.get_or_create(
                    post_id=post_id, article_page=page, original_permalink=original_permalink)

                self.load_primary_topic(post_id, page)
                self.load_additional_topics(post_id, page)

                revision = page.save_revision(
                    user=None,
                    submitted_for_moderation=False,
                )
                revision.publish()

    def process_html_for_stream_field(self, html):
        processed_html = []
        html = self.process_for_line_breaks(html)
        html = self.process_html_for_images(html, use_image_names=True)
        parser = BeautifulSoup(html, "html5lib")

        # processed_html.extend(self._process_element(parser.body))
        all_children = list(parser.body.children)
        if all_children:
            if len(all_children) > 1:
                all_children = self._join_non_block_children(all_children, 'p')
            for child in all_children:
                processed_html.extend(self._process_element(child))
        else:
            processed_html.extend(self._process_base_element(html))

        return processed_html

    def process_for_line_breaks(self, text):
        line_splits = re.split('\r\n\r\n|\n\n', text)
        line_splits = ["<p>{}</p>".format(x.replace('\n', '<br/>')) for x in line_splits]

        return "".join(line_splits)

    def _process_element(self, html):
        processed_element = []
        if html.name is None:
            processed_element.append(self._create_paragraph(html.strip()))
        elif html.name == 'img':
            processed_element.append(self._process_image_tag(html))
        elif html.name == 'h1' or html.name == 'h2' or html.name == 'h3' \
                or html.name == 'h4' or html.name == 'h5' \
                or html.name == 'h6' or html.name == 'p' \
                or html.name == 'div':
            all_children = list(html.children)
            all_children = self._join_non_block_children(all_children,
                                                         html.name)

            for index, child in enumerate(all_children):
                if self._contains_stream_block(child) and len(
                        all_children) > 1:
                    child_blocks = self._process_element(child)
                    processed_element.extend(child_blocks)
                elif child.name is None:
                    tag = element.Tag(parser="html", name=html.name)
                    tag.string = child
                    processed_element.extend(self._process_base_element(tag))
                else:
                    processed_element.extend(self._process_base_element(child))

        return processed_element

    def _join_non_block_children(self, all_children, parent_tag_name):
        updated_children = []
        last_child_was_block = True

        for child in all_children:
            if isinstance(child, Comment):
                continue
            elif isinstance(child, text_type) and child.strip() == "":
                continue
            elif self._contains_stream_block(child):
                updated_children.append(child)
                last_child_was_block = True
            else:
                if last_child_was_block:
                    tag = element.Tag(parser="html", name=parent_tag_name)
                    tag.contents.append(child)
                    updated_children.append(tag)
                    last_child_was_block = False
                else:
                    last_child = updated_children[-1]
                    last_child.contents.append(child)
        return updated_children

    def _process_base_element(self, html):
        if html.name == 'img':
            return [self._process_image_tag(html)]
        elif html.name == 'h1' or html.name == 'h2' or html.name == 'h3' \
                or html.name == 'h4' or html.name == 'h5' or html.name == 'h6':
            return [{'type': 'Heading', 'value': {'text': html.text, 'heading_level': 2}}]

        elif html.name == 'p' or html.name == 'div':
            inner = html.decode_contents(formatter="html")
            return self._create_paragraph(inner.strip())
        elif html.name is None:
            return self._create_paragraph(html.strip())
        else:
            return self._create_paragraph(html)

    def _create_paragraph(self, text):
        pre, embed, post = self.parse_string_for_embed(text)

        paragraphs = []
        if pre:
            while pre.startswith("<br/>"):
                pre = pre[5:]
            while pre.endswith("<br/>"):
                pre = pre[:len(pre) - 5]
            paragraphs.append(
                {'type': 'Paragraph',
                 'value': {"text": "<p>{}</p>".format(pre),
                           "use_dropcap": False
                           }
                 }
            )
        if embed:
            paragraphs.append(
                {'type': 'Embed',
                 'value': embed
                 }
            )
        if post:
            while post.startswith("<br/>"):
                post = post[5:]
            while post.endswith("<br/>"):
                post = post[:len(post) - 5]
            paragraphs.append(
                {'type': 'Paragraph',
                 'value': {"text": "<p>{}</p>".format(post),
                           "use_dropcap": False
                           }
                 }
            )

        return paragraphs

    def _contains_stream_block(self, html):
        return html.name in ['div', 'p', 'img', 'h1', 'h2', 'h3', 'h4', 'h5',
                             'h6']

    def parse_string_for_embed(self, original_value):
        pre_embed = original_value
        embed_url = ""
        post_embed = ""

        stream_regex = "(?P<pre_embed>.*)(?P<embed>\[stream .* flv=(?P<embed_url>[\w:/\%\.]+) .* /\])(?P<post_embed>.*)"
        result = re.match(stream_regex, original_value)
        if result:
            embed_url = unquote(result.group('embed_url').strip())
            pre_embed = result.group('pre_embed').strip()
            post_embed = result.group('post_embed').strip()

        return pre_embed, embed_url, post_embed

    def _process_image_tag(self, item):
        images = AttributedImage.objects.filter(title=item['src'])
        if images.first():
            return {'type': 'Image', 'value': {'image': images.first().id, 'placement': 'full'}}
        else:
            return {'type': 'Paragraph',
                    'value': {"text": "<p>{}</p>".format(text_type(item)),
                              "use_dropcap": False
                              }
                    }

    def process_html_for_images(self, html, use_image_names=False):
        parser = BeautifulSoup(html, "html5lib")
        image_tags = parser.find_all('img')

        for image_tag in image_tags:
            source = image_tag['src']

            parsed_url = urlparse(source)
            if parsed_url.netloc in self.image_download_domains:

                filename = parsed_url.path.split("/")[-1]

                try:
                    updated_source_url = self.download_image(source, filename,
                                                             use_image_names)

                    html = html.replace(source, updated_source_url)
                except DownloadException as e:
                    if e.response:
                        ImportDownloadError.objects.create(url=e.url, status_code=e.response.status_code)
                    else:
                        ImportDownloadError.objects.create(url=e.url, status_code=404)

        return html

    def download_image(self, url, filename, use_image_names=False):
        try:

            image_records = ImageImport.objects.filter(original_url=url)
            if image_records.count() > 0:
                images = AttributedImage.objects.filter(title=image_records.first().name)
                image = images.first()
            else:
                response = requests.get(url)

                if response.status_code == 200:

                    f = BytesIO(response.content)

                    dim = get_image_dimensions(f)  # (width, height)

                    image = AttributedImage.objects.create(
                        title=filename,
                        uploaded_by_user=None,
                        file=File(f, name=filename),
                        width=dim[0],
                        height=dim[1]
                    )

                    image_record, created = ImageImport.objects.get_or_create(
                        original_url=url, name=image.title)
                    image_record.save()
                else:
                    raise DownloadException(url, response)

            if use_image_names:
                updated_source_url = image.title
            else:
                updated_source_url = image.get_rendition(
                    'width-{}'.format(image.width)).url
            return updated_source_url
        except IOError:
            raise DownloadException(url, None)

    def get_data_for_topics(self, post_id, primary_topic=False):
        taxonomy = 'post_tag'
        if primary_topic:
            taxonomy = 'subject'

        query = "SELECT wp_terms.name, wp_terms.slug " \
                "FROM wp_term_relationships " \
                "INNER JOIN wp_posts " \
                "ON object_id=wp_posts.ID  " \
                "INNER JOIN wp_term_taxonomy " \
                "ON wp_term_taxonomy.term_taxonomy_id=wp_term_relationships.term_taxonomy_id " \
                "INNER JOIN wp_terms " \
                "ON wp_term_taxonomy.term_id=wp_terms.term_id " \
                "WHERE post_status = 'publish' " \
                "AND taxonomy = '{}'" \
                "AND wp_posts.ID = '{}'".format(taxonomy, post_id)

        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def load_primary_topic(self, post_id, post):
        primary_topic_results = self.get_data_for_topics(post_id, primary_topic=True)

        if primary_topic_results:
            for name, original_slug in primary_topic_results:
                new_slug = slugify(name)
                try:
                    topic = Topic.objects.get(slug=new_slug)
                except Topic.DoesNotExist:
                    topic = Topic.objects.create(name=name, slug=new_slug)

                TagImport.objects.get_or_create(topic=topic, original_slug=original_slug)
                post.primary_topic = topic

    def load_additional_topics(self, post_id, post):
        topic_results = self.get_data_for_topics(post_id)

        if topic_results:
            for name, original_slug in topic_results:
                new_slug = slugify(name)
                try:
                    topic = Topic.objects.get(slug=new_slug)
                except Topic.DoesNotExist:
                    topic = Topic.objects.create(name=name, slug=new_slug)

                TagImport.objects.get_or_create(topic=topic, original_slug=original_slug)
                ArticleTopicLink.objects.get_or_create(topic=topic, article=post)

    def load_series_posts(self):
        for post_type in ["In Depth", ]:
            results = self.get_post_data(post_type)

            series_list_page = Page.objects.get(slug="indepth")

            for (post_id, post_content, post_title, post_excerpt, post_name,
                 author_email, post_date) in results:

                cleaned_post_name = unquote(post_name).encode('ascii', 'ignore')

                pages = SeriesPage.objects.filter(slug=cleaned_post_name)
                if pages.count() > 0:
                    page = pages.first()
                else:
                    page = SeriesPage(owner=None)
                    series_list_page.add_child(instance=page)

                if not page.main_image:
                    self.update_post_image_data(page, post_id)

                page.slug = cleaned_post_name

                if post_title:
                    page.title = post_title
                else:
                    page.title = ''
                if post_date:
                    page.first_published_at = timezone.make_aware(post_date, timezone.pytz.timezone('GMT'))
                if post_content:
                    updated_post_content = self.process_html_for_stream_field(
                        post_content)
                    page.body = json.dumps(updated_post_content)
                else:
                    page.body = ''

                revision = page.save_revision(
                    user=None,
                    submitted_for_moderation=False,
                )
                revision.publish()

                original_permalink = "/".join([self.get_category_slug(post_type), post_name])
                import_record, created = PostImport.objects.get_or_create(
                    post_id=post_id, article_page=page, original_permalink=original_permalink)

                if post_content:
                    self.process_html_for_series_links(post_content, page)

                self.load_primary_topic(post_id, page)

                revision = page.save_revision(
                    user=None,
                    submitted_for_moderation=False,
                )
                revision.publish()

    def process_html_for_series_links(self, html, series):
        parser = BeautifulSoup(html, "html5lib")
        link_tags = parser.find_all('a')

        for link_tag in link_tags:
            if link_tag.has_attr('href'):
                link = link_tag['href']
                path_parts = link.strip("/").split("/")
                potential_article_slug = path_parts[-1]
                try:
                    article = ArticlePage.objects.get(slug=potential_article_slug)
                    SeriesArticleLink.objects.get_or_create(article=article, series=series)
                except ArticlePage.DoesNotExist:
                    pass  # skip it as it doesn't seem to exist.


class DownloadException(Exception):
    def __init__(self, url, response):
        self.url = url
        self.response = response
