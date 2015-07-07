from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from articles.models import ArticlePage

from .models import HomePage


class HomePageTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_articles_returns_the_correct_number(self):
        home = HomePage.objects.all().first()
        home.number_of_articles = 2
        home.save()

        self.assertEqual(2, home.articles.count())

    def test_articles_returns_in_order_from_newest_to_oldest(self):
        home = HomePage.objects.all().first()
        home.number_of_articles = 2
        home.save()

        expected = [
            ArticlePage.objects.get(pk=108),
            ArticlePage.objects.get(pk=107),
        ]

        self.assertSequenceEqual(home.articles, expected)
