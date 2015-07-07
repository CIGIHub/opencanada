from __future__ import absolute_import, unicode_literals

from django.test import TestCase


class HomePageTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_articles_returns_the_correct_number(self):
        pass

    def test_articles_returns_in_order_from_newest_to_oldest(self):
        pass
