from __future__ import absolute_import, unicode_literals

from wagtail.core import blocks
from wagtail.core.fields import StreamField


class BioField(StreamField):
    def __init__(self, block_types=None, **kwargs):
        block_types = [
            ('Paragraph', blocks.RichTextBlock(icon="doc-full")),
        ]

        super(BioField, self).__init__(block_types, **kwargs)
