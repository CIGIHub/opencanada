from django.test import TestCase

from .models import EventPage


class EventPageTestCase(TestCase):

    def test_str_returns_title(self):
        page = EventPage(title="This is an Event page.")
        self.assertEqual(str(page), "This is an Event page.")
