from __future__ import absolute_import, unicode_literals

from os import environ

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from wordpress_importer.utils import get_setting


class TestUtils(TestCase):
    def testLoadingSetEnvironmentVariable(self):
        environ["WP_IMPORTER_SOME_VARIABLE"] = "This value"
        value = get_setting("SOME_VARIABLE")
        self.assertEqual("This value", value)

    def testUnsetVariableThrowsImproperlyConfigured(self):
        self.assertRaises(ImproperlyConfigured, get_setting, "SOME_UNSET_VARIABLE")

    def testLoadingSetDjangoSetting(self):
        with self.settings(WP_IMPORTER_SOME_VARIABLE_SET_IN_SETTINGS='Something awesome'):
            value = get_setting("SOME_VARIABLE_SET_IN_SETTINGS")
            self.assertEqual("Something awesome", value)
