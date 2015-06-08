from __future__ import absolute_import, unicode_literals

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock


class BodyField(StreamField):
    def __init__(self, block_types=None, **kwargs):
        block_types = [
            ('Heading', blocks.CharBlock(icon="title", classname="heading")),
            ('Paragraph', blocks.RichTextBlock(icon="doc-full")),
            ('Image', ImageChooserBlock(icon="image")),
            ('Embed', EmbedBlock(icon="site")),
            ('List', blocks.ListBlock(blocks.RichTextBlock(label="item"), icon="list-ul")),
            ('Sharable', blocks.CharBlock(icon="openquote")),
            # TODO: do we want to have the author blurb placed by the editor or algorithmically placed?
        ]

        super(BodyField, self).__init__(block_types, **kwargs)
