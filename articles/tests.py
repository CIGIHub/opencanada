from django.test import TestCase

from people.models import Contributor

from .models import (ArticleListPage, ArticlePage, ArticleTopicLink,
                     InDepthListPage, InDepthPage, Topic)


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

    def test_topics_includes_allprimary_and_secondary_topics(self):
        indepth = InDepthPage.objects.all().first()
        topics = indepth.topics

        t1 = Topic.objects.get(pk=1)
        t2 = Topic.objects.get(pk=2)
        t4 = Topic.objects.get(pk=4)
        self.assertIn(t1, topics)
        self.assertIn(t2, topics)
        self.assertIn(t4, topics)

    def test_topics_sorted_alphabetically(self):
        indepth = InDepthPage.objects.all().first()
        topics = indepth.topics
        self.assertEqual("Topic 1", topics[0].name)
        self.assertEqual("Topic 2", topics[1].name)
        self.assertEqual("Topic 4", topics[2].name)

    def test_topics_removes_duplicates(self):
        indepth = InDepthPage.objects.all().first()
        self.assertEqual(len(indepth.topics), 3)


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

    def test_topics_includes_allprimary_and_secondary_topics(self):
        article = ArticlePage.objects.get(slug="test-article-4")
        self.assertEqual(len(article.topics), 3)

        t1 = Topic.objects.get(pk=1)
        t2 = Topic.objects.get(pk=2)
        t3 = Topic.objects.get(pk=3)
        self.assertIn(t1, article.topics)
        self.assertIn(t2, article.topics)
        self.assertIn(t3, article.topics)

    def test_topics_sorted_alphabetically(self):
        article = ArticlePage.objects.get(slug="test-article-4")
        topics = article.topics
        self.assertEqual("Topic 1", topics[0].name)
        self.assertEqual("Topic 2", topics[1].name)
        self.assertEqual("Topic 3", topics[2].name)

    def test_topics_removes_duplicates(self):
        article = ArticlePage.objects.get(slug="test-article-3")
        self.assertEqual(len(article.topics), 1)


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


class ArticleTopicLinkTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_str(self):
        link = ArticleTopicLink.objects.get(pk=1)
        self.assertEqual("Test Article 4 - Topic 2", str(link))
