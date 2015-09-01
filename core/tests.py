from __future__ import absolute_import, unicode_literals

from django.test import Client, TestCase

from articles.models import ArticlePage, SeriesPage

from .models import HomePage


class HomePageTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_articles_returns_the_correct_number(self):
        home = HomePage.objects.all().first()
        home.number_of_rows_of_articles = 2
        home.number_of_columns_of_articles = 1
        home.save()

        self.assertEqual(2, len(home.articles))

    def test_articles_returns_in_order_from_newest_to_oldest(self):
        home = HomePage.objects.all().first()
        home.number_of_rows_of_articles = 2
        home.number_of_columns_of_articles = 1
        home.save()

        expected = [
            [SeriesPage.objects.get(pk=116), ],
            [ArticlePage.objects.get(pk=108), ],
        ]

        self.assertSequenceEqual(home.articles, expected)

    def test_articles_returns_sticky_articles_first(self):
        home = HomePage.objects.all().first()
        home.number_of_rows_of_articles = 2
        home.number_of_columns_of_articles = 1
        home.save()

        sticky_page = SeriesPage.objects.get(pk=110)
        sticky_page.sticky = True
        sticky_page.save()

        expected = [
            [SeriesPage.objects.get(pk=110), ],
            [SeriesPage.objects.get(pk=116), ],
        ]

        self.assertSequenceEqual(home.articles, expected)

    def test_articles_returns_in_rows(self):
        home = HomePage.objects.all().first()
        home.number_of_rows_of_articles = 5
        home.number_of_columns_of_articles = 3
        home.save()

        expected = [
            [SeriesPage.objects.get(pk=116),
             ArticlePage.objects.get(pk=108),
             ArticlePage.objects.get(pk=115), ],
            [ArticlePage.objects.get(pk=107), ],
            [ArticlePage.objects.get(pk=109), ],
            [ArticlePage.objects.get(pk=111), ],
        ]

        self.assertSequenceEqual(home.articles, expected)

    def test_articles_returns_in_sub_rows(self):
        home = HomePage.objects.all().first()
        home.number_of_rows_of_articles = 3
        home.number_of_columns_of_articles = 4
        home.save()

        sticky_page = ArticlePage.objects.get(pk=107)
        sticky_page.sticky = True
        sticky_page.save()

        expected = [
            [
                ArticlePage.objects.get(pk=107),
                [
                    [SeriesPage.objects.get(pk=116), ],
                    [ArticlePage.objects.get(pk=108), ],
                ]
            ],
            [
                ArticlePage.objects.get(pk=109),
                ArticlePage.objects.get(pk=115)
            ],
        ]

        self.assertSequenceEqual(home.articles, expected)

    def test_fill_row_1(self):
        home = HomePage.objects.all().first()

        articles = SeriesPage.objects.live().all().order_by("-first_published_at")

        expected = [SeriesPage.objects.get(pk=116)]
        actual, height = home._fill_row(1, articles, [], 1)

        self.assertSequenceEqual(actual, expected)
        self.assertEqual(height, 1)

    def test_fill_row_2(self):
        home = HomePage.objects.all().first()

        articles = SeriesPage.objects.live().all().order_by("-first_published_at")

        expected = [SeriesPage.objects.get(pk=116), SeriesPage.objects.get(pk=110), ]
        actual, height = home._fill_row(2, articles, [], 1)

        self.assertSequenceEqual(actual, expected)
        self.assertEqual(height, 1)

    def test_feed(self):
        client = Client()
        resp = client.get('/feed/')

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<title>In Depth Articles - No Topic - Not Live</title>', resp.content)
