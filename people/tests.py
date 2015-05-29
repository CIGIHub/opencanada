from django.test import TestCase

from . import models


class ContributorTestCase(TestCase):
    def testNoRequiredFields(self):
        contributor = models.Contributor.objects.create()
        contributor.save()
