from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from articles.models import Topic
from wordpress_importer.models import ImageImport, PostImport, TagImport


class PostImportTestCast(TestCase):
    def test_str_returns_post_id(self):
        post_import = PostImport(post_id=1093)

        self.assertEqual(str(post_import), "1093")


class ImageImportTestCase(TestCase):
    def test_str_returns_name(self):
        image_import = ImageImport(original_url="http://example.com/cat.jpg", name="cat.jpg")

        self.assertEqual(str(image_import), "cat.jpg")


class TagImportTestCase(TestCase):
    def test_str_returns_slug_tag_name(self):
        topic, created = Topic.objects.get_or_create(name="Topic 1")
        tag_import = TagImport(original_slug="my-slug", topic=topic)

        self.assertEqual(str(tag_import), "my-slug - Topic 1")
