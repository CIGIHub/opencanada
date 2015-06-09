# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from collections import namedtuple

import mock
import six
from django.conf import settings
from django.test import TestCase
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import Image

from articles.models import ArticlePage
from people.models import Contributor
from wordpress_importer.management.commands import import_from_wordpress


class ImageCleanUp(object):
    def delete_images(self):
        # clean up any image files that were created.
        images = Image.objects.all()

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


@mock.patch('requests.get', local_get_successful)
class TestCommandImportFromWordPressLoadContributors(TestCase, ImageCleanUp):
    def setUp(self):
        import_from_wordpress.Command.get_contributor_data = self.get_test_contributor_data

    def tearDown(self):
        self.delete_images()

    def testLoadContributorsCreatesContributor(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = Contributor.objects.filter(email='bob@example.com')
        self.assertEqual(1, contributors.count())

    def testLoadContributorsSetsFirstName(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = Contributor.objects.filter(email='bob@example.com')
        self.assertEqual('Bob', contributors.first().first_name)

    def testLoadContributorsSetsLastName(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = Contributor.objects.filter(email='bob@example.com')
        self.assertEqual('Smith', contributors.first().last_name)

    def testLoadContributorsSetsNickname(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = Contributor.objects.filter(email='bob@example.com')
        self.assertEqual('Bobby Smith', contributors.first().nickname)

    def testLoadContributorsSetsTwitterHandle(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = Contributor.objects.filter(email='bob@example.com')
        self.assertEqual('@bobsmith', contributors.first().twitter_handle)

    def testLoadContributorsSetsShortBio(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = Contributor.objects.filter(email='bob@example.com')
        self.assertEqual('Bob Smith is a person who does stuff.',
                         contributors.first().short_bio)

    def testLoadContributorsSetsImageFile(self):
        command = import_from_wordpress.Command()
        command.load_contributors()
        contributors = Contributor.objects.filter(email='bob@example.com')

        images = Image.objects.filter(title='testcat.jpg')
        self.assertEqual(1, images.count())
        self.assertEqual(images.first(), contributors.first().headshot)

    # TODO: Long Bio
    # TODO: multiple contributors

    def get_test_contributor_data(self):
        data = [
            ('bob@example.com', 'first_name', 'Bob'),
            ('bob@example.com', 'last_name', 'Smith'),
            ('bob@example.com', 'nickname', 'Bobby Smith'),
            ('bob@example.com', 'twitter', '@bobsmith'),
            ('bob@example.com', 'description',
             'Bob Smith is a person who does stuff.'),
            ('bob@example.com', 'userphoto_image_file', 'testcat.jpg'),
        ]
        return data


@mock.patch('requests.get', local_get_successful)
class TestCommandImportFromWordPressLoadPosts(TestCase, ImageCleanUp):
    fixtures = ['test.json']

    def setUp(self):
        import_from_wordpress.Command.get_post_data = self.get_test_post_data

    def tearDown(self):
        self.delete_images()

    def testCreatesPageWithSlug(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        self.assertEqual(1, pages.count())

    def testPageIsChildOfFeatures(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        features_page = Page.objects.get(slug='features')

        self.assertTrue(pages.first().is_descendant_of(features_page))
        # self.assertTrue(pages.first().path.startswith(features_page.path))

    def testPageSetsTitle(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        self.assertEqual('Is NATO Ready for Putin?', pages.first().title)

    def testPageSetsBody(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        self.assertEqual(
            [("Paragraph", "<p>Vladimir Putin has challenged</p>"), ],
            pages.first().body.stream_data)

    # TODO: various aspects of setting body:  long

    def testPageSetsExcerptContainingUnicode(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        self.assertEqual(
            'Political hurdles hold NATO back — how convenient for Russian tactics.',
            pages.first().excerpt)

    def testPageImportsHTML(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='html-post')
        self.assertEqual('The excerpt also has some <strong>HTML</strong>.',
                         pages.first().excerpt)
        self.assertEqual(
            [("Paragraph", '<p>This <strong>is</strong></p>'),
             ("Paragraph",
              '<p><img src="http://www.example.com/test.jpg"/></p>'),
             ("Paragraph",
              '<p>a <a href="http://www.example.com">post</a> <span class="special">that has html</span></p>'),
             ("Paragraph", '<p>Yay!</p>'), ],
            pages.first().body.stream_data)

    def testPageUpdatesLocalImageUrls(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='html-local-image-post')

        images = Image.objects.filter(title='testcat.jpg')

        self.assertEqual(
            [('Image', images.first()),
             ("Paragraph", "<p>a cat</p>"),
             ],
            pages.first().body.stream_data)

    def testPageNullFields(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='null-fields')
        self.assertEqual('', pages.first().excerpt)
        self.assertEqual([], pages.first().body.stream_data)
        self.assertEqual('', pages.first().title)

    def testPageBlankFields(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='blank-fields')
        self.assertEqual('', pages.first().excerpt)
        self.assertEqual([], pages.first().body.stream_data)
        self.assertEqual('', pages.first().title)

    def testPageHasAuthor(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        contributors = Contributor.objects.filter(email='bob@example.com')
        self.assertEqual(pages.first().author, contributors.first())

    def testPageAuthorNotSet(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='null-author')
        self.assertEqual(pages.first().author, None)

    def testPageEmptyAuthor(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='empty-author')
        self.assertEqual(pages.first().author, None)

    def testPageNonExistantAuthor(self):
        # TODO: should this cause an error
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='nonexistant-author')
        self.assertEqual(pages.first().author, None)

    def testUpdatesDuplicateSlug(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = ArticlePage.objects.filter(slug='duplicate')
        self.assertEqual(pages.count(), 1)
        self.assertEqual(pages.first().title, "title 2")

    # TODO: Multiple Authors? Is that a thing on OpenCanada?

    # TODO: Tags

    def get_test_post_data(self):
        data = [
            ('Vladimir Putin has challenged',
             'Is NATO Ready for Putin?',
             'Political hurdles hold NATO back — how convenient for Russian tactics.',
             'is-nato-ready-for-putin',
             'bob@example.com',),
            (
                '<p>This <strong>is</strong> <img src="http://www.example.com/test.jpg" /> a <a href="http://www.example.com">post</a> <span class="special">that has html</span></p><div>Yay!</div>',
                'HTML Works?',
                'The excerpt also has some <strong>HTML</strong>.',
                'html-post',
                'bob@example.com',),
            (None,
             None,
             None,
             'null-fields',
             'bob@example.com',
             ),
            ('',
             '',
             '',
             'blank-fields',
             'bob@example.com',
             ),
            ('body',
             'title',
             'excerpt',
             'null-author',
             None,
             ),
            ('body',
             'title',
             'excerpt',
             'empty-author',
             '',
             ),
            ('body',
             'title',
             'excerpt',
             'nonexistant-author',
             'doesnotexist@here.com',
             ),
            ('body',
             'title',
             'excerpt',
             'duplicate',
             'bob@example.com',
             ),
            ('body',
             'title 2',
             'excerpt',
             'duplicate',
             'bob@example.com',
             ),
            ('<div><img src="{}" />a cat</div>'.format(test_image_url),
             'title',
             'excerpt',
             'html-local-image-post',
             'bob@example.com',),
        ]
        return data


@mock.patch('requests.get', local_get_successful)
class TestCommandImportProcessHTMLForImages(TestCase, ImageCleanUp):
    def tearDown(self):
        self.delete_images()

    def testHTMLHasImageImageCreatedWhenDownloaded(self):
        command = import_from_wordpress.Command()
        html = "<div><img src='{}'></div>".format(test_image_url)
        command.process_html_for_images(html)

        images = Image.objects.filter(title='testcat.jpg')

        self.assertEqual(1, images.count())

    def testHTMLImageSourceUpdatedWhenDownloaded(self):
        command = import_from_wordpress.Command()
        html = "<div><img src='{}'></div>".format(test_image_url)
        html = command.process_html_for_images(html)

        images = Image.objects.filter(title='testcat.jpg')

        self.assertEqual(html, "<div><img src='{}'></div>".format(
            images.first().get_rendition('width-100').url))

    def testImageNotDownloadedForRemote(self):
        command = import_from_wordpress.Command()
        html = "<div><img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test.jpg'></div>"
        command.process_html_for_images(html)
        images = Image.objects.filter(title='Test.jpg')

        self.assertEqual(0, images.count())

    def testHTMLNotUpdatedForRemote(self):
        command = import_from_wordpress.Command()
        html = "<div><img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test.jpg'></div>"
        html = command.process_html_for_images(html)

        self.assertEqual(html,
                         "<div><img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test.jpg'></div>")

    def testHTMLWithUnicodeNoUpload(self):
        command = import_from_wordpress.Command()
        html = "<div><p>€</p><img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test€.jpg'></div>"
        html = command.process_html_for_images(html)

        self.assertEqual(html,
                         "<div><p>€</p><img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test€.jpg'></div>")

    # def testHTMLWithUnicodeImageSourceUpdatedWhenDownloaded(self):
    #     command = import_from_wordpress.Command()
    #     html = "<div<img src='{}'></div>".format(test_image_url_with_unicode)
    #     html = command.process_html_for_images(html)
    #
    #     images = Image.objects.filter(title='testcat♥.jpg')
    #
    #     self.assertEqual(1, images.count())
    #
    #     self.assertEqual(html, "<div><img src='{}'></div>".format(
    #         images.first().get_rendition('width-100').url))


class TestCommandImportDownloadImage(TestCase, ImageCleanUp):
    def tearDown(self):
        self.delete_images()

    @mock.patch('requests.get', local_get_successful)
    def testImageCreatedWhenDownloaded(self):
        command = import_from_wordpress.Command()
        command.download_image(test_image_url, 'testcat.jpg')

        images = Image.objects.filter(title='testcat.jpg')

        self.assertEqual(1, images.count())

    @mock.patch('requests.get', local_get_404)
    def testDownloadExceptionWhenError(self):
        command = import_from_wordpress.Command()
        self.assertRaises(import_from_wordpress.DownloadException,
                          command.download_image,
                          'file:///{}/wordpress_importer/tests/files/purple.jpg'.format(
                              settings.PROJECT_ROOT), 'purple.jpg')


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
              "value": "<p>This is a simple paragraph.</p>"}],
            processed
        )

    def testImageUploadedLocally(self):
        command = import_from_wordpress.Command()
        html = "<img src='{}' />".format(test_image_url)
        processed = command.process_html_for_stream_field(html)

        images = Image.objects.filter(title='testcat.jpg')
        self.assertEqual(1, images.count())

        self.assertEqual(processed, [{"type": "Image",
                                      "value": 1}, ])

    def testImageWithParagraphs(self):
        command = import_from_wordpress.Command()
        html = "<p>This is a simple paragraph.</p><img src='{}' /><p>This is a second paragraph.</p>".format(
            test_image_url)
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{"type": "Paragraph",
              "value": "<p>This is a simple paragraph.</p>"},
             {"type": "Image",
              "value": 1},
             {"type": "Paragraph",
              "value": "<p>This is a second paragraph.</p>"},
             ],
            processed
        )

    def testImageInParagraph(self):
        command = import_from_wordpress.Command()
        html = "<p>This is a paragraph. <img src='{}' /> This is a second paragraph.</p>".format(
            test_image_url)
        # import pdb; pdb.set_trace()
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{"type": "Paragraph",
              "value": "<p>This is a paragraph.</p>"},
             {"type": "Image",
              "value": 1},
             {"type": "Paragraph",
              "value": "<p>This is a second paragraph.</p>"},
             ],
            processed
        )

    def testExternalImage(self):
        command = import_from_wordpress.Command()
        html = "<p>This is a simple paragraph.</p><img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test.jpg' /><p>This is a second paragraph.</p>"
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{"type": "Paragraph",
              "value": "<p>This is a simple paragraph.</p>"},
             {"type": "Paragraph",
              "value": '<p><img src="http://upload.wikimedia.org/wikipedia/en/b/bd/Test.jpg"/></p>'},
             {"type": "Paragraph",
              "value": "<p>This is a second paragraph.</p>"},
             ],
            processed
        )

    def testDivs(self):
        command = import_from_wordpress.Command()
        html = "<div>This is a simple paragraph.</div><div>This is a second paragraph.</div>"
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{"type": "Paragraph",
              "value": "<p>This is a simple paragraph.</p>"},
             {"type": "Paragraph",
              "value": "<p>This is a second paragraph.</p>"},
             ],
            processed
        )

    def testNonBlockTagStrong(self):
        command = import_from_wordpress.Command()
        html = "<p>This is a <strong>simple paragraph.</strong></p>"
        processed = command.process_html_for_stream_field(html)

        self.assertEqual(
            [{"type": "Paragraph",
              "value": "<p>This is a <strong>simple paragraph.</strong></p>"},
             ],
            processed
        )

    def testNonAndBlockSubTags(self):
        command = import_from_wordpress.Command()
        html = '<p>This <strong>is</strong> <img src="http://www.example.com/test.jpg" /></p>'
        processed = command.process_html_for_stream_field(html)
        self.assertEqual(
            [{"type": "Paragraph", "value": '<p>This <strong>is</strong></p>'},
             {"type": "Paragraph",
              "value": '<p><img src="http://www.example.com/test.jpg"/></p>'},
             ],
            processed)
