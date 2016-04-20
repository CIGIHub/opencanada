import io

from django.core.exceptions import SuspiciousFileOperation
from django.template.base import TemplateDoesNotExist
from django.template.utils import get_app_template_dirs
from django.utils._os import safe_join

"""
We need a way to verify that a custom template exists as part of a Theme.
Based on django.template.loaders.app_directories.Loader
"""
class CustomTemplateChecker(object):

    def __init__(self, file_charset='utf-8'):
        self.file_charset = file_charset

    def get_absolute_path(self, template_name, template_dirs=None):
        for file_path in self.get_template_sources(template_name, template_dirs):
            try:
                with io.open(file_path, encoding=self.file_charset) as fp:
                    return file_path
            except IOError:
                pass
        raise TemplateDoesNotExist(template_name)

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """
        if not template_dirs:
            template_dirs = get_app_template_dirs('templates')
        for template_dir in template_dirs:
            try:
                yield safe_join(template_dir, template_name)
            except SuspiciousFileOperation:
                # The joined path was located outside of this template_dir
                # (it might be inside another one, so this isn't fatal).
                pass
