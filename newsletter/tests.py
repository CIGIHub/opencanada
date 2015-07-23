from datetime import datetime

from django.test import TestCase

from .models import NewsletterPage


class ArticleListPageTestCase(TestCase):

    def test_str_returns_title(self):
        page = NewsletterPage(title="This is a Newsletter page.", issue_date=datetime(2015, 7, 25))
        self.assertEqual(str(page), "2015-07-25")
