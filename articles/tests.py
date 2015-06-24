from django.test import TestCase

from people.models import Contributor

from .models import ArticleListPage, ArticlePage, InDepthListPage, InDepthPage


class InDepthPageTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_has_right_number_of_authors(self):
        indepth = InDepthPage.objects.all().first()
        self.assertEqual(len(indepth.authors), 2)

    def test_has_right_authors_from_articles(self):
        indepth = InDepthPage.objects.all().first()
        bob = Contributor.objects.get(email="bobsmith@example.com")
        joe = Contributor.objects.get(email="joesampson@example.com")
        self.assertEqual(indepth.authors, [bob, joe])

    # TODO: verify articles in the series, order
    # TODO: verify overridden details for articles


class ArticlePageTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_single_author_has_one_author(self):
        article = ArticlePage.objects.get(slug="test-article-1")
        self.assertEqual(len(article.authors), 1)

    def test_single_author_has_expected_author(self):
        article = ArticlePage.objects.get(slug="test-article-1")
        bob = Contributor.objects.get(email="bobsmith@example.com")
        self.assertEqual(article.authors[0], bob)

    def test_multiple_authors(self):
        article = ArticlePage.objects.get(slug="test-article-4")
        self.assertEqual(len(article.authors), 2)

    def test_single_author_has_expected_author_in_order(self):
        article = ArticlePage.objects.get(slug="test-article-4")
        mary = Contributor.objects.get(email="marysue@example.com")
        joe = Contributor.objects.get(email="joesampson@example.com")

        self.assertEqual(article.authors[0], mary)
        self.assertEqual(article.authors[1], joe)

#   TODO: verify series articles, order, overridden details
#   TODO: verify related articles
#


class ArticleListPageTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_get_list_of_articles(self):
        features = ArticleListPage.objects.get(slug='features')
        articles = features.subpages
        self.assertEqual(len(articles), 4)


class InDepthListPageTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_get_list_of_indepths(self):
        indepth = InDepthListPage.objects.get(slug='indepth')
        indepth_pages = indepth.subpages
        self.assertEqual(len(indepth_pages), 1)
