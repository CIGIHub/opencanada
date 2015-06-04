# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import Image

from core.models import LegacyArticlePage
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

        images = Image.objects.filter(title='50')
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
            ('bob@example.com', 'userphoto_image_file', '50'),
        ]
        return data


class TestCommandImportFromWordPressLoadPosts(TestCase, ImageCleanUp):
    fixtures = ['test.json']

    def setUp(self):
        import_from_wordpress.Command.get_post_data = self.get_test_post_data

    def tearDown(self):
        self.delete_images()

    def testCreatesLegacyPageWithSlug(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        self.assertEqual(1, pages.count())

    def testPageIsChildOfFeatures(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        features_page = Page.objects.get(slug='features')

        self.assertTrue(pages.first().is_descendant_of(features_page))
        # self.assertTrue(pages.first().path.startswith(features_page.path))

    def testPageSetsTitle(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        self.assertEqual('Is NATO Ready for Putin?', pages.first().title)

    def testPageSetsBody(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        self.assertEqual('Vladimir Putin has challenged', pages.first().body)

    # TODO: various aspects of setting body:  long

    def testPageSetsExcerptContainingUnicode(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        self.assertEqual(
            'Political hurdles hold NATO back — how convenient for Russian tactics.',
            pages.first().excerpt)

    def testPageImportsHTML(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(slug='html-post')
        self.assertEqual('The excerpt also has some <strong>HTML</strong>.',
                         pages.first().excerpt)
        self.assertEqual(
            '<p>This <strong>is</strong> <img src="http://www.example.com/test.jpg" /> a <a href="http://www.example.com">post</a> <span class="special">that has html</span></p><div>Yay!</div>',
            pages.first().body)

    def testPageUpdatesLocalImageUrls(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(slug='html-local-image-post')

        images = Image.objects.filter(title='300')

        self.assertEqual(
            '<div><img src="{}" />a cat</div>'.format(images.first().get_rendition('width-200').url),
            pages.first().body)

    def testPageNullFields(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(slug='null-fields')
        self.assertEqual('', pages.first().excerpt)
        self.assertEqual('', pages.first().body)
        self.assertEqual('', pages.first().title)

    def testPageBlankFields(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(slug='blank-fields')
        self.assertEqual('', pages.first().excerpt)
        self.assertEqual('', pages.first().body)
        self.assertEqual('', pages.first().title)

    def testPageHasAuthor(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(
            slug='is-nato-ready-for-putin')
        contributors = Contributor.objects.filter(email='bob@example.com')
        self.assertEqual(pages.first().author, contributors.first())

    def testPageAuthorNotSet(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(slug='null-author')
        self.assertEqual(pages.first().author, None)

    def testPageEmptyAuthor(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(slug='empty-author')
        self.assertEqual(pages.first().author, None)

    def testPageNonExistantAuthor(self):
        # TODO: should this cause an error
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(slug='nonexistant-author')
        self.assertEqual(pages.first().author, None)

    def testUpdatesDuplicateSlug(self):
        command = import_from_wordpress.Command()
        command.load_posts()
        pages = LegacyArticlePage.objects.filter(slug='duplicate')
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
            ('<div><img src="http://placekitten.com/g/200/300" />a cat</div>',
             'title',
             'excerpt',
             'html-local-image-post',
             'bob@example.com',),
        ]
        return data


class TestCommandImportProcessHTMLForImages(TestCase, ImageCleanUp):

    def tearDown(self):
        self.delete_images()

    def testHTMLHasImageImageCreatedWhenDownloaded(self):
        command = import_from_wordpress.Command()
        html = "<div><img src='http://placekitten.com/g/200/300'></div>"
        command.process_body_html_for_images(html)

        images = Image.objects.filter(title='300')

        self.assertEqual(1, images.count())

    def testHTMLImageSourceUpdatedWhenDownloaded(self):
        command = import_from_wordpress.Command()
        html = "<div><img src='http://placekitten.com/g/200/300'></div>"
        html = command.process_body_html_for_images(html)

        images = Image.objects.filter(title='300')

        self.assertEqual(html, "<div><img src='{}'></div>".format(images.first().get_rendition('width-200').url))

    def testImageNotDownloadedForRemote(self):
        command = import_from_wordpress.Command()
        html = "<div><img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test.jpg'></div>"
        command.process_body_html_for_images(html)
        images = Image.objects.filter(title='Test.jpg')

        self.assertEqual(0, images.count())

    def testHTMLNotUpdatedForRemote(self):
        command = import_from_wordpress.Command()
        html = "<div><img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test.jpg'></div>"
        html = command.process_body_html_for_images(html)

        self.assertEqual(html, "<div><img src='http://upload.wikimedia.org/wikipedia/en/b/bd/Test.jpg'></div>")


class TestCommandImportDownloadImage(TestCase, ImageCleanUp):

    def tearDown(self):
        self.delete_images()

    def testImageCreatedWhenDownloaded(self):
        command = import_from_wordpress.Command()
        command.download_image('http://placekitten.com/g/200/300', '300')

        images = Image.objects.filter(title='300')

        self.assertEqual(1, images.count())

    def testDownloadExceptionWhenError(self):
        command = import_from_wordpress.Command()
        self.assertRaises(import_from_wordpress.DownloadException, command.download_image, 'http://placekitten.com/g/200/purple', 'purple')
