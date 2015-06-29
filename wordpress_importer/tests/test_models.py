from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from wordpress_importer.models import ImageImport, PostImport


class PostImportTestCast(TestCase):
    def test_str_returns_post_id(self):
        post_import = PostImport(post_id=1093)

        self.assertEqual(str(post_import), "1093")


class ImageImportTestCase(TestCase):
    def test_str_returns_name(self):
        image_import = ImageImport(original_url="http://example.com/cat.jpg", name="cat.jpg")

        self.assertEqual(str(image_import), "cat.jpg")
