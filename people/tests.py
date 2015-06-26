from django.test import TestCase

from . import models


class ContributorTestCase(TestCase):
    def test_title_from_name(self):
        contributor = models.ContributorPage.objects.create(first_name="Bob", last_name="Smith", depth=1)
        contributor.save()

        self.assertEqual(contributor.title, "Bob Smith")
