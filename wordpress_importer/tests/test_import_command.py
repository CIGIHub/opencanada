# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
from collections import namedtuple

import mock
import six
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from wagtail.wagtailcore.models import Page

from articles.models import ArticleCategory, ArticlePage
from images.models import AttributedImage
from people.models import ContributorPage
from wordpress_importer.management.commands import import_from_wordpress
from wordpress_importer.models import (ImageImport, ImportDownloadError,
                                       PostImport)


class ImageCleanUp(object):
    def delete_images(self):
        # clean up any image files that were created.
        images = AttributedImage.objects.all()

        for image in images:
            storage, path = image.file.storage, image.file.path
            image.delete()
            storage.delete(path)


FakeResponse = namedtuple('FakeResponse', 'status_code, content')


def local_get_successful(url):
    "Fetch a stream from local files."
    p_url = six.moves.urllib.parse.urlparse(url)
    if p_url.scheme != 'file':
        raise ValueError("Expected file scheme")

    filename = six.moves.urllib.request.url2pathname(p_url.path)

    response = FakeResponse(200, open(filename, 'rb').read())
    return response


def local_get_404(url):
    "Fetch a stream from local files."

    response = FakeResponse(404, None)
    return response


test_image_url = 'file:///{}/wordpress_importer/tests/files/testcat.jpg'.format(
    settings.PROJECT_ROOT)
test_image_url_with_unicode = 'file:///{}/wordpress_importer/tests/files/testcat♥.jpg'.format(
    settings.PROJECT_ROOT)


class TestCommandImportFromWordPressLoadContributors(TestCase, ImageCleanUp):
    def setUp(self):
        import_from_wordpress.Command.get_contributor_data = self.get_test_contributor_data

    def tearDown(self):
        self.delete_images()

    @mock.patch('requests.get', local_get_successful)
    def testLoadContributorsCreatesContributor(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = ContributorPage.objects.filter(email='bob@example.com')
        self.assertEqual(1, contributors.count())

    @mock.patch('requests.get', local_get_successful)
    def testLoadContributorsSetsFirstName(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = ContributorPage.objects.filter(email='bob@example.com')
        self.assertEqual('Bob', contributors.first().first_name)

    @mock.patch('requests.get', local_get_successful)
    def testLoadContributorsSetsLastName(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = ContributorPage.objects.filter(email='bob@example.com')
        self.assertEqual('Smith', contributors.first().last_name)

    @mock.patch('requests.get', local_get_successful)
    def testLoadContributorsSetsNickname(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = ContributorPage.objects.filter(email='bob@example.com')
        self.assertEqual('Bobby Smith', contributors.first().nickname)

    @mock.patch('requests.get', local_get_successful)
    def testLoadContributorsSetsTwitterHandle(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = ContributorPage.objects.filter(email='bob@example.com')
        self.assertEqual('@bobsmith', contributors.first().twitter_handle)

    @mock.patch('requests.get', local_get_successful)
    def testLoadContributorsSetsTwitterHandleFromUrl(self):
        import_from_wordpress.Command.get_contributor_data = self.get_test_contributor_data_twitter_url
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = ContributorPage.objects.filter(email='bob@example.com')
        self.assertEqual('@bobsmith', contributors.first().twitter_handle)

    @mock.patch('requests.get', local_get_successful)
    def testLoadContributorsSetsLongBio(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = ContributorPage.objects.filter(email='bob@example.com')
        self.assertEqual('Bob Smith is a person who does stuff.',
                         contributors.first().long_bio)

    @mock.patch('requests.get', local_get_successful)
    def testLoadContributorsSetsShortBio(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = ContributorPage.objects.filter(email='bob@example.com')
        self.assertEqual('He does stuff.',
                         contributors.first().short_bio)

    # @mock.patch('requests.get', local_get_successful)
    # def testLoadContributorsSetsImageFile(self):
    #     command = import_from_wordpress.Command()
    #     command.load_contributors()
    #     contributors = ContributorPage.objects.filter(email='bob@example.com')
    #
    #     images = AttributedImage.objects.filter(title='testcat.jpg')
    #     self.assertEqual(1, images.count())
    #     self.assertEqual(images.first(), contributors.first().headshot)
    #
    # @mock.patch('requests.get', local_get_404)
    # def testDownloadErrorLoggedWhenErrorGettingImage(self):
    #     command = import_from_wordpress.Command()
    #     command.load_contributors()
    #
    #     errors = ImportDownloadError.objects.all()
    #     self.assertEqual(1, errors.count())
    #     self.assertEqual(404, errors.first().status_code)
    #     self.assertEqual(settings.WP_IMPORTER_USER_PHOTO_URL_PATTERN.format("testcat.jpg"), errors.first().url)

    def get_test_contributor_data(self):
        data = [
            ('bob@example.com', 'first_name', 'Bob'),
            ('bob@example.com', 'last_name', 'Smith'),
            ('bob@example.com', 'nickname', 'Bobby Smith'),
            ('bob@example.com', 'twitter', '@bobsmith'),
            ('bob@example.com', 'description',
             'Bob Smith is a person who does stuff.'),
            ('bob@example.com', 'SHORT_BIO',
             'He does stuff.'),
            ('bob@example.com', 'userphoto_image_file', 'testcat.jpg'),
        ]
        return data

    def get_test_contributor_data_twitter_url(self):
        data = [
            ('bob@example.com', 'first_name', 'Bob'),
            ('bob@example.com', 'last_name', 'Smith'),
            ('bob@example.com', 'nickname', 'Bobby Smith'),
            ('bob@example.com', 'TWITTER', 'https://twitter.com/bobsmith'),
            ('bob@example.com', 'description',
             'Bob Smith is a person who does stuff.'),
            ('bob@example.com', 'SHORT_BIO',
             'He does stuff.'),
            ('bob@example.com', 'userphoto_image_file', 'testcat.jpg'),
        ]
        return data


@mock.patch('requests.get', local_get_successful)
class TestCommandImportFromWordPressUnicodeSlug(TestCase, ImageCleanUp):
    def setUp(self):
        import_from_wordpress.Command.get_post_data = self.get_test_post_data
        import_from_wordpress.Command.get_post_image_data = self.get_test_post_image_data
        import_from_wordpress.Command.get_data_for_topics = self.get_test_data_for_topics

    def tearDown(self):
        self.delete_images()

    def testCreatesPageWithAsciiSlug(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='crisis-at-home-for-canadas-armed-forces')
        self.assertEqual(1, pages.count())

    def get_test_post_data(self, post_type):
        data = [
            (1,
             'Crisis At Home',
             'Test?',
             'Body.',
             "crisis-at-home-for-canadas-armed-forces%e2%80%a8",
             'bob@example.com',
             datetime.datetime(2011, 2, 22, 5, 48, 31),
             ),
        ]
        return data

    def get_test_post_image_data(self, post_id):
        return None

    def get_test_data_for_topics(self, post_id, primary_topic=False):
        return (
            ('Topic 1', 'topic-1'),
        )


class TestCommandImportFromWordPressLoadPosts(TestCase, ImageCleanUp):
    fixtures = ['test.json']

    def setUp(self):
        import_from_wordpress.Command.get_post_data = self.get_test_post_data
        import_from_wordpress.Command.get_post_image_data = self.get_test_post_image_data
        import_from_wordpress.Command.get_data_for_topics = self.get_test_data_for_topics
        import_from_wordpress.Command.get_category_data = self.get_test_category_data

    def tearDown(self):
        self.delete_images()

    @mock.patch('requests.get', local_get_successful)
    def testCreatesPageWithSlug(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        self.assertEqual(1, pages.count())

    @mock.patch('requests.get', local_get_successful)
    def testPageIsChildOfFeatures(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        features_page = Page.objects.get(slug='features')

        self.assertTrue(pages.first().is_descendant_of(features_page))

    @mock.patch('requests.get', local_get_successful)
    def testPageSetsTitle(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        self.assertEqual('Is NATO Ready for Putin?', pages.first().title)

    @mock.patch('requests.get', local_get_successful)
    def testPageSetsBody(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        self.assertEqual(
            [{'type': "Paragraph", 'value': {"text": "<p>Vladimir Putin has challenged</p>", "use_dropcap": False}}, ],
            pages.first().body.stream_data)

    @mock.patch('requests.get', local_get_successful)
    def testPageSetsExcerptContainingUnicode(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        self.assertEqual(
            'Political hurdles hold NATO back — how convenient for Russian tactics.',
            pages.first().excerpt)

    @mock.patch('requests.get', local_get_successful)
    def testPageImportsHTML(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='html-post')
        self.assertEqual('The excerpt also has some <strong>HTML</strong>.',
                         pages.first().excerpt)
        self.assertEqual(
            [{"type": "Paragraph", "value": {'text': '<p>This <strong>is</strong></p>', 'use_dropcap': False}},
             {"type": "Paragraph",
              "value": {'text': '<p><img src="http://www.example.com/test.jpg"/></p>', 'use_dropcap': False}},
             {"type": "Paragraph",
              "value": {'text': '<p>a <a href="http://www.example.com">post</a><span class="special">that has html</span></p>', 'use_dropcap': False}},
             {"type": "Paragraph", "value": {'text': '<p>Yay!</p>', 'use_dropcap': False}}, ],
            pages.first().body.stream_data)

    @mock.patch('requests.get', local_get_successful)
    def testPageUpdatesLocalImageUrls(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='html-local-image-post')

        images = AttributedImage.objects.filter(title='testcat.jpg')

        self.assertEqual(
            [{'type': 'Image', 'value': {'image': images.first().id, 'placement': 'full', 'expandable': False, 'label': None}},
             {'type': "Paragraph", 'value': {"text": "<p>a cat</p>", 'use_dropcap': False}},
             ],
            pages.first().body.stream_data)

    @mock.patch('requests.get', local_get_404)
    def testDownloadErrorLoggedWhenErrorGettingImage(self):
        command = import_from_wordpress.Command()
        command.load_posts()

        errors = ImportDownloadError.objects.filter(url=test_image_url)
        self.assertEqual(404, errors.first().status_code)

    @mock.patch('requests.get', local_get_successful)
    def testPageNullFields(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='null-fields')
        self.assertEqual('', pages.first().excerpt)
        self.assertEqual([], pages.first().body.stream_data)
        self.assertEqual('', pages.first().title)

    @mock.patch('requests.get', local_get_successful)
    def testPageBlankFields(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='blank-fields')
        self.assertEqual('', pages.first().excerpt)
        self.assertEqual([], pages.first().body.stream_data)
        self.assertEqual('', pages.first().title)

    @mock.patch('requests.get', local_get_successful)
    def testPageHasAuthor(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        contributors = ContributorPage.objects.filter(email='bob@example.com')
        self.assertEqual(pages.first().author_links.count(), 1)
        self.assertEqual(pages.first().author_links.first().author, contributors.first())

    @mock.patch('requests.get', local_get_successful)
    def testPageAuthorNotSet(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='null-author')
        self.assertEqual(pages.first().author_links.count(), 0)

    @mock.patch('requests.get', local_get_successful)
    def testPageEmptyAuthor(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='empty-author')
        self.assertEqual(pages.first().author_links.count(), 0)

    @mock.patch('requests.get', local_get_successful)
    def testPageNonExistantAuthor(self):
        # TODO: should this cause an error
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='nonexistant-author')
        self.assertEqual(pages.first().author_links.count(), 0)

    @mock.patch('requests.get', local_get_successful)
    def testUpdatesDuplicateSlug(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='duplicate')
        self.assertEqual(pages.count(), 1)
        self.assertEqual(pages.first().title, "title 2")

    @mock.patch('requests.get', local_get_successful)
    def testImportTrackingCreated(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        imports = PostImport.objects.filter(post_id=5)
        self.assertEqual(imports.count(), 1)

    @mock.patch('requests.get', local_get_successful)
    def testSetsDate(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        self.assertEqual(
            timezone.datetime(2011, 2, 22, 5, 48, 31, tzinfo=timezone.pytz.timezone('GMT')),
            pages.first().first_published_at)

    @mock.patch('requests.get', local_get_successful)
    def testDefaultCategorySet(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        page = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin').first()
        default_category = ArticleCategory.objects.get(slug="feature")
        self.assertEqual(default_category, page.category)

    @mock.patch('requests.get', local_get_successful)
    def testSetsPrimaryTopic(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        page = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin').first()

        self.assertEqual("Primary Topic 1", page.primary_topic.name)

    @mock.patch('requests.get', local_get_successful)
    def testSetsSecondaryTopics(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        page = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin').first()

        self.assertEqual(1, page.topic_links.count())
        self.assertEqual("Secondary Topic 1", page.topic_links.first().topic.name)

    def get_test_post_image_data(self, post_id):
        return None

    def get_test_category_data(self):
        return (
            ("Features", 1, "features", 0),
            ("Essays", 3, "essays", 0),
            ("101s", 4, "101", 0),
            ("Roundtable", 5, "roundtable", 0),
            ("Dispatch", 6, "roundtable", 0),
            ("Comments", 7, "roundtable", 0),
            ("Essays", 6, "roundtable", 0),
            ("Visualizations", 9, "roundtable", 0),
            ("Interviews", 10, "roundtable", 0),
            ("Rapid Response Group", 11, "roundtable", 0),
            ("Graphics", 2, "graphics", 1),
        )

    def get_test_data_for_topics(self, post_id, primary_topic=False):
        if primary_topic:
            return (
                ('Primary Topic 1', 'primary-topic-1'),
            )
        else:
            return (
                ('Secondary Topic 1', 'secondary-topic-1'),
            )

    def get_test_post_data(self, post_type):
        if post_type == "Features":
            data = [
                (1,
                 'Vladimir Putin has challenged',
                 'Is NATO Ready for Putin?',
                 'Political hurdles hold NATO back — how convenient for Russian tactics.',
                 'is-nato-ready-for-putin',
                 'bob@example.com',
                 datetime.datetime(2011, 2, 22, 5, 48, 31),
                 ),
                (2,
                 '<p>This <strong>is</strong> <img src="http://www.example.com/test.jpg" /> a <a href="http://www.example.com">post</a><span class="special">that has html</span></p><div>Yay!</div>',
                 'HTML Works?',
                 'The excerpt also has some <strong>HTML</strong>.',
                 'html-post',
                 'bob@example.com',
                 datetime.datetime(2011, 2, 22, 5, 48, 31),
                 ),
                (3,
                 None,
                 None,
                 None,
                 'null-fields',
                 'bob@example.com',
                 datetime.datetime(2011, 2, 22, 5, 48, 31),
                 ),
                (5,
                 '',
                 '',
                 '',
                 'blank-fields',
                 'bob@example.com',
                 datetime.datetime(2011, 2, 22, 5, 48, 31),
                 ),
                (6,
                 'body',
                 'title',
                 'excerpt',
                 'null-author',
                 None,
                 datetime.datetime(2011, 2, 22, 5, 48, 31),
                 ),
                (7,
                 'body',
                 'title',
                 'excerpt',
                 'empty-author',
                 '',
                 datetime.datetime(2011, 2, 22, 5, 48, 31),
                 ),
                (8,
                 'body',
                 'title',
                 'excerpt',
                 'nonexistant-author',
                 'doesnotexist@here.com',
                 datetime.datetime(2011, 2, 22, 5, 48, 31),
                 ),
                (9,
                 'body',
                 'title',
                 'excerpt',
                 'duplicate',
                 'bob@example.com',
                 datetime.datetime(2011, 2, 22, 5, 48, 31),
                 ),
                (10,
                 'body',
                 'title 2',
                 'excerpt',
                 'duplicate',
                 'bob@example.com',
                 datetime.datetime(2011, 2, 22, 5, 48, 31),
                 ),
                (11,
                 '<div><img src="{}" />a cat</div>'.format(test_image_url),
                 'title',
                 'excerpt',
                 'html-local-image-post',
                 'bob@example.com',
                 datetime.datetime(2011, 2, 22, 5, 48, 31),
                 ),
            ]
        else:
            data = []
        return data


class TestCommandImportProcessHTMLForImages(TestCase, ImageCleanUp):
    def tearDown(self):
        self.delete_images()

    @mock.patch('requests.get', local_get_successful)
    def testHTMLHasImageImageCreatedWhenDownloaded(self):
        command = import_from_wordpress.Command()
        html = "<img src='{}'/>".format(test_image_url)
        command.process_html_for_images(html)

        images = AttributedImage.objects.filter(title='testcat.jpg')

        self.assertEqual(1, images.count())

    @mock.patch('requests.get', local_get_successful)
    def testHTMLImageSourceUpdatedWhenDownloaded(self):
        command = import_from_wordpress.Command()
        html = "<img src='{}'/>".format(test_image_url)
        html = command.process_html_for_images(html)

        images = AttributedImage.objects.filter(title='testcat.jpg')

        self.assertEqual(html, "<img src='{}'/>".format(
            images.first().get_rendition('width-100').url))

    @mock.patch('requests.get', local_get_successful)
    def testImageNotDownloadedForRemote(self):
        command = import_from_wordpress.Command()
        html = "<img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test.jpg'/>"
        command.process_html_for_images(html)
        images = AttributedImage.objects.filter(title='Test.jpg')

        self.assertEqual(0, images.count())

    @mock.patch('requests.get', local_get_successful)
    def testHTMLNotUpdatedForRemote(self):
        command = import_from_wordpress.Command()
        html = "<img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test.jpg'/>"
        html = command.process_html_for_images(html)

        self.assertEqual(html,
                         "<img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test.jpg'/>")

    @mock.patch('requests.get', local_get_successful)
    def testHTMLWithUnicodeNoUpload(self):
        command = import_from_wordpress.Command()
        html = "<p>€</p><img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test€.jpg'/>"
        html = command.process_html_for_images(html)

        self.assertEqual(html,
                         "<p>€</p><img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test€.jpg'/>")

    @mock.patch('requests.get', local_get_successful)
    def testHTMLWithUnicodeImageSourceUpdatedWhenDownloaded(self):
        command = import_from_wordpress.Command()
        html = "<img src='{}' />".format(test_image_url_with_unicode)
        html = command.process_html_for_images(html)

        images = AttributedImage.objects.filter(title='testcat♥.jpg')

        self.assertEqual(1, images.count())

        self.assertEqual(html, "<img src='{}' />".format(
            images.first().get_rendition('width-100').url))

    @mock.patch('requests.get', local_get_404)
    def testDownloadErrorLoggedWhenError(self):
        command = import_from_wordpress.Command()
        html = "<img src='{}' />".format(test_image_url_with_unicode)
        html = command.process_html_for_images(html)

        errors = ImportDownloadError.objects.filter(url=test_image_url_with_unicode)

        self.assertEqual(1, errors.count())
        self.assertEqual(404, errors.first().status_code)


class TestCommandImportDownloadImage(TestCase, ImageCleanUp):
    def tearDown(self):
        self.delete_images()

    @mock.patch('requests.get', local_get_successful)
    def testImageCreatedWhenDownloaded(self):
        command = import_from_wordpress.Command()
        command.download_image(test_image_url, 'testcat.jpg')

        images = AttributedImage.objects.filter(title='testcat.jpg')

        self.assertEqual(1, images.count())

    @mock.patch('requests.get', local_get_404)
    def testDownloadExceptionWhenError(self):
        command = import_from_wordpress.Command()
        with self.assertRaises(import_from_wordpress.DownloadException):
            command.download_image(
                'file:///{}/wordpress_importer/tests/files/purple.jpg'.format(
                    settings.PROJECT_ROOT),
                'purple.jpg'
            )

    @mock.patch('requests.get', local_get_404)
    def testDownloadExceptionHasDetails(self):
        command = import_from_wordpress.Command()
        try:
            command.download_image(
                'file:///{}/wordpress_importer/tests/files/purple.jpg'.format(
                    settings.PROJECT_ROOT),
                'purple.jpg'
            )
        except import_from_wordpress.DownloadException as e:
            self.assertEqual(
                'file:///{}/wordpress_importer/tests/files/purple.jpg'.format(
                    settings.PROJECT_ROOT), e.url)
            self.assertEqual(e.response.status_code, 404)

    @mock.patch('requests.get', local_get_successful)
    def testImageImportRecordCreatedWhenDownloaded(self):
        command = import_from_wordpress.Command()
        command.download_image(test_image_url, 'testcat.jpg')

        image_records = ImageImport.objects.filter(name='testcat.jpg')

        self.assertEqual(1, image_records.count())


@mock.patch('requests.get', local_get_successful)
class TestCommandProcessHTLMForStreamField(TestCase, ImageCleanUp):
    def tearDown(self):
        self.delete_images()

    def testSimpleParagraph(self):
        command = import_from_wordpress.Command()
        html = "<p>This is a simple paragraph.</p>"
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{"type": "Paragraph",
              "value": {"text": "<p>This is a simple paragraph.</p>", 'use_dropcap': False}}],
            processed
        )

    def testImageUploadedLocally(self):
        command = import_from_wordpress.Command()
        html = "<img src='{}' />".format(test_image_url)
        processed = command.process_html_for_stream_field(html)

        images = AttributedImage.objects.filter(title='testcat.jpg')
        self.assertEqual(1, images.count())

        self.assertEqual(processed, [{"type": "Image",
                                      "value": {'image': 1, 'placement': 'full'}}, ])

    def testImageWithParagraphs(self):
        command = import_from_wordpress.Command()
        html = "<p>This is a simple paragraph.</p><img src='{}' /><p>This is a second paragraph.</p>".format(
            test_image_url)
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{"type": "Paragraph",
              "value": {"text": "<p>This is a simple paragraph.</p>", 'use_dropcap': False}},
             {"type": "Image",
              "value": {'image': 1, 'placement': 'full'}},
             {"type": "Paragraph",
              "value": {"text": "<p>This is a second paragraph.</p>", 'use_dropcap': False}},
             ],
            processed
        )

    def testImageInParagraph(self):
        command = import_from_wordpress.Command()
        html = "<p>This is a paragraph. <img src='{}' /> This is a second paragraph.</p>".format(
            test_image_url)
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{"type": "Paragraph",
              "value": {"text": "<p>This is a paragraph.</p>", 'use_dropcap': False}},
             {"type": "Image",
              "value": {'image': 1, 'placement': 'full'}},
             {"type": "Paragraph",
              "value": {"text": "<p>This is a second paragraph.</p>", 'use_dropcap': False}},
             ],
            processed
        )

    def testExternalImage(self):
        command = import_from_wordpress.Command()
        html = "<p>This is a simple paragraph.</p><img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test.jpg' /><p>This is a second paragraph.</p>"
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{"type": "Paragraph",
              "value": {"text": "<p>This is a simple paragraph.</p>", 'use_dropcap': False}},
             {"type": "Paragraph",
              "value": {"text": '<p><img src="http://upload.wikimedia.org/wikipedia/en/b/bd/Test.jpg"/></p>', 'use_dropcap': False}},
             {"type": "Paragraph",
              "value": {"text": "<p>This is a second paragraph.</p>", 'use_dropcap': False}},
             ],
            processed
        )

    def testDivs(self):
        command = import_from_wordpress.Command()
        html = "<div><div>This is a simple paragraph.</div><img src='{}' /><div>This is a second paragraph.<img src='{}' /></div></div>".format(
            test_image_url, test_image_url)
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{"type": "Paragraph",
              "value": {"text": "<p>This is a simple paragraph.</p>", 'use_dropcap': False}},
             {"type": "Image",
              "value": {'image': 1, 'placement': 'full'}},
             {"type": "Paragraph",
              "value": {"text": "<p>This is a second paragraph.</p>", 'use_dropcap': False}},
             {"type": "Image",
              "value": {'image': 1, 'placement': 'full'}},
             ],
            processed
        )

    def testHeaders(self):
        command = import_from_wordpress.Command()
        html = "<h1>This is a header 1</h1><h2>This is a header 2</h2>" \
               "<h3>This is a header 3</h3><h4>This is a header 4</h4>" \
               "<h5>This is a header 5</h5><h6>This is a header 6</h6>"
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{"type": "Heading",
              "value": {'text': "This is a header 1", 'heading_level': 2}},
             {"type": "Heading",
              "value": {'text': "This is a header 2", 'heading_level': 2}},
             {"type": "Heading",
              "value": {'text': "This is a header 3", 'heading_level': 2}},
             {"type": "Heading",
              "value": {'text': "This is a header 4", 'heading_level': 2}},
             {"type": "Heading",
              "value": {'text': "This is a header 5", 'heading_level': 2}},
             {"type": "Heading",
              "value": {'text': "This is a header 6", 'heading_level': 2}},
             ],
            processed
        )

    def testImagesInHeaders(self):
        command = import_from_wordpress.Command()
        html = "<h2><img src='{}' />This is the heading</h2>".format(
            test_image_url)
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{"type": "Image",
              "value": {'image': 1, 'placement': 'full'}},
             {"type": "Heading",
              "value": {'text': "This is the heading", 'heading_level': 2}},
             ],
            processed
        )

    def testImagesInHeadersFollowingText(self):
        command = import_from_wordpress.Command()
        html = "<h2>This is the heading<img src='{}' /></h2>".format(
            test_image_url)
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [
                {"type": "Heading",
                 "value": {'text': "This is the heading", 'heading_level': 2}},
                {"type": "Image",
                 "value": {'image': 1, 'placement': 'full'}},
            ],
            processed
        )

    def testImagesInHeadersWrappedInText(self):
        command = import_from_wordpress.Command()
        html = "<h2>This is the heading<img src='{0}' />This is more heading<img src='{0}' />This is even more heading</h2>".format(
            test_image_url)
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [
                {"type": "Heading",
                 "value": {'text': "This is the heading", 'heading_level': 2}},
                {"type": "Image",
                 "value": {'image': 1, 'placement': 'full'}},
                {"type": "Heading",
                 "value": {'text': "This is more heading", 'heading_level': 2}},
                {"type": "Image",
                 "value": {'image': 1, 'placement': 'full'}},
                {"type": "Heading",
                 "value": {'text': "This is even more heading", 'heading_level': 2}},
            ],
            processed
        )

    def testNonBlockTagStrong(self):
        command = import_from_wordpress.Command()
        html = "<p>This is a <strong>simple paragraph.</strong></p>"
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{"type": "Paragraph",
              "value": {"text": "<p>This is a <strong>simple paragraph.</strong></p>", 'use_dropcap': False}},
             ],
            processed
        )

    def testNonAndBlockSubTags(self):
        command = import_from_wordpress.Command()
        html = '<p>This <strong>is</strong> <img src="http://www.example.com/test.jpg" /></p>'
        processed = command.process_html_for_stream_field(html)
        self.assertEqual(
            [{"type": "Paragraph", "value": {"text": '<p>This <strong>is</strong></p>', 'use_dropcap': False}},
             {"type": "Paragraph",
              "value": {"text": '<p><img src="http://www.example.com/test.jpg"/></p>', 'use_dropcap': False}},
             ],
            processed)

    def testExtraWhiteSpaceIsRemoved(self):
        command = import_from_wordpress.Command()
        html = "  <p>Test</p>         <div>Second</div>  &nbsp;   <p>Third</p>"
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{'type': 'Paragraph', 'value': {"text": '<p>Test</p>', 'use_dropcap': False}},
             {'type': 'Paragraph', 'value': {"text": '<p>Second</p>', 'use_dropcap': False}},
             {'type': 'Paragraph', 'value': {"text": '<p>Third</p>', 'use_dropcap': False}},
             ],
            processed
        )

    def testCommentsOutsideStructureAreRemoved(self):
        command = import_from_wordpress.Command()
        html = '&nbsp;<!--more-->    <p>This has a <!--more--> comment</p>'
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{'type': 'Paragraph', 'value': {'text': '<p>This has a  comment</p>', 'use_dropcap': False}}],
            processed
        )

    def testSimpleCommentsAreRemoved(self):
        command = import_from_wordpress.Command()
        html = '<p>This has a <!--more--> comment</p>'
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{'type': 'Paragraph', 'value': {"text": '<p>This has a  comment</p>', 'use_dropcap': False}}],
            processed
        )

    def testStringsWithNoTagsWithRNBreaks(self):
        command = import_from_wordpress.Command()
        html = "This is text.\r\n\r\nThat should be in paragraphs."
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{'type': 'Paragraph', 'value': {"text": '<p>This is text.</p>', 'use_dropcap': False}},
             {'type': 'Paragraph',
              'value': {"text": '<p>That should be in paragraphs.</p>', 'use_dropcap': False}}],
            processed
        )

    def testStringsWithNoTagsWithNNBreaks(self):
        command = import_from_wordpress.Command()
        html = "This is text.\n\nThat should be in paragraphs."
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{'type': 'Paragraph', 'value': {"text": '<p>This is text.</p>', 'use_dropcap': False}},
             {'type': 'Paragraph',
              'value': {"text": '<p>That should be in paragraphs.</p>', 'use_dropcap': False}}],
            processed
        )

    def testStringsWithNoTagsWithNBreaks(self):
        command = import_from_wordpress.Command()
        html = """This is text.\nThat should be in paragraphs."""
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{'type': 'Paragraph',
              'value': {"text": '<p>This is text.<br/>That should be in paragraphs.</p>', 'use_dropcap': False}}],
            processed
        )

    def testNoExtraLineBreakks(self):
        command = import_from_wordpress.Command()
        html = """As one of Canada's principal security and intelligence agencies.
<h4>What is CSE?</h4>
Little is known about CSE because of secrecy."""
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{'type': 'Paragraph',
              'value': {"text": "<p>As one of Canada's principal security and intelligence agencies.</p>", 'use_dropcap': False}},
             {'type': 'Heading',
              'value': {"text": 'What is CSE?', 'heading_level': 2}},
             {'type': 'Paragraph',
              'value': {"text": '<p>Little is known about CSE because of secrecy.</p>', 'use_dropcap': False}}

             ],
            processed
        )


class TestProcessForLineBreaks(TestCase):
    def testStringNoTags(self):
        command = import_from_wordpress.Command()
        html = "This is a string."
        processed = command.process_for_line_breaks(html)
        self.assertEqual("<p>This is a string.</p>", processed)

    def testStringsWithNoTagsWithRNBreaks(self):
        command = import_from_wordpress.Command()
        html = "This is text.\r\n\r\nThat should be in paragraphs."
        processed = command.process_for_line_breaks(html)

        self.assertEqual(
            "<p>This is text.</p><p>That should be in paragraphs.</p>",
            processed
        )

    def testStringsWithNoTagsWithNNBreaks(self):
        command = import_from_wordpress.Command()
        html = "This is text.\n\nThat should be in paragraphs."
        processed = command.process_for_line_breaks(html)

        self.assertEqual(
            "<p>This is text.</p><p>That should be in paragraphs.</p>",
            processed
        )

    def testStringsWithNoTagsWithNBreaks(self):
        command = import_from_wordpress.Command()
        html = "This is text.\nThat has a line break."
        processed = command.process_for_line_breaks(html)

        self.assertEqual(
            "<p>This is text.<br/>That has a line break.</p>",
            processed
        )


class TestGetDownloadPathAndFilename(TestCase):
    def testNoSubFolderReturnsFilenameAndUrl(self):
        command = import_from_wordpress.Command()
        url, filename = command.get_download_path_and_filename(
            "http://example.com/uploads/my_image.jpg",
            "http://newdomain.com/images/{}"
        )

        self.assertEqual("http://newdomain.com/images/my_image.jpg", url)
        self.assertEqual("my_image.jpg", filename)

    def testSubFolderReturnsFilenameAndUrlWithSubfolders(self):
        command = import_from_wordpress.Command()
        url, filename = command.get_download_path_and_filename(
            "http://example.com/uploads/2011/04/my_image.jpg",
            "http://newdomain.com/images/{}"
        )

        self.assertEqual("http://newdomain.com/images/2011/04/my_image.jpg", url)
        self.assertEqual("2011_04_my_image.jpg", filename)


class TestParseEmbed(TestCase):
    def testParagraphWithStreamDataReturnsURL(self):
        command = import_from_wordpress.Command()

        pre, url, post = command.parse_string_for_embed('[stream provider=youtube flv=http%3A//www.youtube.com/watch%3Fv%3DdiTubVRKdz0 embed=false share=false width=646 height=390 dock=true controlbar=over bandwidth=high autostart=false /]')
        self.assertEqual('http://www.youtube.com/watch?v=diTubVRKdz0', url)
        self.assertEqual('', pre)
        self.assertEqual('', post)

    def testEmbedWithPreAndPost(self):
        command = import_from_wordpress.Command()

        pre, url, post = command.parse_string_for_embed('Stuff before the embed. [stream provider=youtube flv=http%3A//www.youtube.com/watch%3Fv%3DdiTubVRKdz0 embed=false share=false width=646 height=390 dock=true controlbar=over bandwidth=high autostart=false /] Stuff after the embed.')
        self.assertEqual('http://www.youtube.com/watch?v=diTubVRKdz0', url)
        self.assertEqual('Stuff before the embed.', pre)
        self.assertEqual('Stuff after the embed.', post)

    def testNoEmbed(self):
        command = import_from_wordpress.Command()

        pre, url, post = command.parse_string_for_embed('Just a regular paragraph.')
        self.assertEqual('', url)
        self.assertEqual('Just a regular paragraph.', pre)
        self.assertEqual('', post)
