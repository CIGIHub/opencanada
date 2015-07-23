from django.test import TestCase
from django.utils import six

from images.models import AttributedImage
from people.models import ContributorPage

from .models import (ArticleAuthorLink, ArticleListPage, ArticlePage,
                     ArticleTopicLink, Headline, SeriesListPage, SeriesPage,
                     Topic, TopicListPage)


class SeriesPageTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_has_right_number_of_authors(self):
        series = SeriesPage.objects.all().first()
        self.assertEqual(len(series.authors), 2)

    def test_has_right_authors_from_articles(self):
        series = SeriesPage.objects.all().first()
        bob = ContributorPage.objects.get(email="bobsmith@example.com")
        joe = ContributorPage.objects.get(email="joesampson@example.com")

        self.assertIn(bob, series.authors)
        self.assertIn(joe, series.authors)

    def test_authors_in_alphabetical_order(self):
        series = SeriesPage.objects.all().first()
        bob = ContributorPage.objects.get(email="bobsmith@example.com")
        joe = ContributorPage.objects.get(email="joesampson@example.com")

        self.assertEqual(joe, series.authors[0])
        self.assertEqual(bob, series.authors[1])

        bob.last_name = "Achange"

        revision = bob.save_revision(
            user=None,
            submitted_for_moderation=False,
        )
        revision.publish()

        self.assertEqual(bob, series.authors[0])
        self.assertEqual(joe, series.authors[1])

    def test_series_articles(self):
        series = SeriesPage.objects.all().first()

        a6 = ArticlePage.objects.get(pk=107)
        a7 = ArticlePage.objects.get(pk=108)

        self.assertEqual(2, len(series.articles))

        self.assertIn(a6, series.articles)
        self.assertIn(a7, series.articles)

    def test_series_articles_order(self):
        series = SeriesPage.objects.all().first()

        a6 = ArticlePage.objects.get(pk=107)
        a7 = ArticlePage.objects.get(pk=108)

        self.assertEqual(a7, series.articles[0])
        self.assertEqual(a6, series.articles[1])

    def test_article_has_override_text(self):
        series = SeriesPage.objects.all().first()

        override = series.articles[0].override_text

        self.assertEqual("<p>This is overridden text.</p>", override)

    def test_article_has_override_image(self):
        series = SeriesPage.objects.all().first()

        image = AttributedImage.objects.get(pk=1)
        override = series.articles[0].override_image

        self.assertEqual(image, override)

    def test_topics_includes_allprimary_and_secondary_topics(self):
        series = SeriesPage.objects.all().first()
        topics = series.topics

        t1 = Topic.objects.get(pk=1)
        t2 = Topic.objects.get(pk=2)
        t4 = Topic.objects.get(pk=4)
        self.assertIn(t1, topics)
        self.assertIn(t2, topics)
        self.assertIn(t4, topics)

    def test_topics_sorted_alphabetically(self):
        series = SeriesPage.objects.all().first()
        topics = series.topics
        self.assertEqual("Topic 1", topics[0].name)
        self.assertEqual("Topic 2", topics[1].name)
        self.assertEqual("Topic 4", topics[2].name)

    def test_topics_removes_duplicates(self):
        series = SeriesPage.objects.all().first()
        self.assertEqual(len(series.topics), 3)

    def test_topics_when_non_set_returns_empty_list(self):
        series = SeriesPage.objects.get(slug="depth-articles-no-topics")
        self.assertEqual(series.topics, [])

    def test_related_articles_gets_matching_primary_topics(self):
        indepth = SeriesPage.objects.all().first()
        related_articles = indepth.related_articles(number=2)

        self.assertEqual(related_articles[0].primary_topic, indepth.primary_topic)

    def test_related_articles_returns_the_number_requested(self):
        series = SeriesPage.objects.all().first()
        related_articles = series.related_articles(number=2)
        self.assertEqual(2, len(related_articles))

    def test_str_returns_title(self):
        page = SeriesPage(title="This is a title.")
        self.assertEqual("This is a title.", str(page))


class ArticlePageTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_str_returns_title(self):
        article = ArticlePage(title="This is a title.")
        self.assertEqual("This is a title.", str(article))

    def test_single_author_has_one_author(self):
        article = ArticlePage.objects.get(slug="test-article-1")
        self.assertEqual(len(article.authors), 1)

    def test_single_author_has_expected_author(self):
        article = ArticlePage.objects.get(slug="test-article-1")
        bob = ContributorPage.objects.get(email="bobsmith@example.com")
        self.assertEqual(article.authors[0], bob)

    def test_multiple_authors(self):
        article = ArticlePage.objects.get(slug="test-article-4")
        self.assertEqual(len(article.authors), 2)

    def test_single_author_has_expected_author_in_order(self):
        article = ArticlePage.objects.get(slug="test-article-4")
        mary = ContributorPage.objects.get(email="marysue@example.com")
        joe = ContributorPage.objects.get(email="joesampson@example.com")

        self.assertEqual(article.authors[0], mary)
        self.assertEqual(article.authors[1], joe)

#   TODO: verify related articles

    def test_related_articles_returns_the_number_requested(self):
        article = ArticlePage.objects.get(id=109)
        related_articles = article.related_articles(number=2)
        self.assertEqual(2, len(related_articles))

    def test_related_articles_excludes_self(self):
        article = ArticlePage.objects.get(id=109)
        related_articles = article.related_articles(number=10)
        self.assertNotIn(article, related_articles)

    # TODO: Includes primary topic as filter
    # TODO: Includes secondary topics as filter
    # TODO: Includes authors as filter

    def test_series_contains_series(self):
        article = ArticlePage.objects.get(pk=107)
        series = SeriesPage.objects.all().first()
        actual = article.series_articles
        self.assertEqual(1, len(actual))
        self.assertEqual(series, actual[0][0])

    def test_other_articles_in_series(self):
        article = ArticlePage.objects.get(pk=107)
        other_article = ArticlePage.objects.get(pk=108)
        actual = article.series_articles
        self.assertIn(other_article, actual[0][1])

    def test_series_artcles_does_not_contain_self(self):
        article = ArticlePage.objects.get(pk=107)
        actual = article.series_articles
        self.assertNotIn(article, actual[0][1])

    def test_article_has_override_text_for_series_related(self):
        article = ArticlePage.objects.get(pk=107)
        override = article.series_articles[0][1][0].override_text
        self.assertEqual("<p>This is overridden text.</p>", override)

    def test_article_has_override_image_for_series_related(self):
        article = ArticlePage.objects.get(pk=107)
        image = AttributedImage.objects.get(pk=1)
        override = article.series_articles[0][1][0].override_image
        self.assertEqual(image, override)

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

    def test_topics_when_non_set_returns_empty_list(self):
        article = ArticlePage.objects.get(slug="no-topics")

        self.assertEqual(article.topics, [])


class ArticleListPageTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_get_list_of_articles(self):
        features = ArticleListPage.objects.get(slug='features')
        articles = features.subpages
        self.assertEqual(len(articles), 5)

    def test_str_returns_title(self):
        page = ArticleListPage(title="This is a List Page.")
        self.assertEqual(str(page), "This is a List Page.")


class SeriesListPageTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_str_returns_title(self):
        page = SeriesListPage(title="This is a title.")
        self.assertEqual("This is a title.", str(page))

    def test_get_list_of_series(self):
        series = SeriesListPage.objects.get(slug='indepth')
        series_pages = series.subpages
        self.assertEqual(len(series_pages), 2)


class ArticleTopicLinkTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_str(self):
        link = ArticleTopicLink.objects.get(pk=1)
        self.assertEqual("Test Article 4 - Topic 2", str(link))


class ArticleAuthorLinkTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_str(self):
        link = ArticleAuthorLink.objects.get(pk=1)
        self.assertEqual("Test Article 1 - Bob Smith", str(link))


class TopicTestCase(TestCase):
    def test_str_returns_title(self):
        topic = Topic(name="Topic 1")
        self.assertEqual(str(topic), "Topic 1")


class TopicListPageTestCase(TestCase):
    fixtures = ["articlestest.json", ]

    def test_str_returns_title(self):
        page = TopicListPage(title="Topics")
        self.assertEqual(str(page), "Topics")

    def test_topics_contains_all_topics(self):
        topics_page = TopicListPage.objects.get(slug='topics')
        all_topics = Topic.objects.all()

        six.assertCountEqual(self, all_topics, topics_page.topics)

    def test_topics_in_alphabetical_order(self):
        topics_page = TopicListPage.objects.get(slug='topics')

        topic_1 = Topic.objects.get(slug="topic-1")
        topic_2 = Topic.objects.get(slug="topic-2")
        topic_3 = Topic.objects.get(slug="topic-3")
        topic_4 = Topic.objects.get(slug="topic-4")

        six.assertCountEqual(
            self,
            topics_page.topics,
            [topic_1, topic_2, topic_3, topic_4]
        )


class HeadlineTestCase(TestCase):
    def test_str_returns_id(self):
        page = TopicListPage.objects.all().first()
        headline = Headline.objects.create(containing_page=page)

        self.assertEqual(str(headline), '1')
