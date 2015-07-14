from __future__ import absolute_import, unicode_literals

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock


class BodyField(StreamField):
    def __init__(self, block_types=None, **kwargs):
        block_types = [
            ('Heading', HeadingBlock()),
            ('Paragraph', ParagraphBlock()),
            ('Image', ImageBlock()),
            ('Embed', EmbedBlock(icon="site")),
            ('List', blocks.ListBlock(
                blocks.RichTextBlock(label="item"), icon="list-ul")
             ),
            ('Sharable', SharableBlock()),
            ('AuthorBlurb', AuthorBlurbBlock()),
        ]

        super(BodyField, self).__init__(block_types, **kwargs)


class HeadingBlock(blocks.StructBlock):
    text = blocks.CharBlock()
    heading_level = blocks.ChoiceBlock(
        choices=[
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
            (6, "6"),
        ],
        default=2
    )

    class Meta:
        template = "articles/blocks/heading.html"
        icon = "title"


class SharableBlock(blocks.CharBlock):
    class Meta:
        template = "articles/blocks/sharable.html"
        icon = "openquote"


class AuthorBlurbBlock(blocks.CharBlock):
    class Meta:
        template = "articles/blocks/author_blurb.html"
        icon = "user"


class ParagraphBlock(blocks.StructBlock):
    text = blocks.RichTextBlock()
    use_dropcap = blocks.BooleanBlock(required=False)

    class Meta:
        template = "articles/blocks/paragraph_block.html"
        icon = "doc-full"


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    placement = blocks.ChoiceBlock(choices=[
        ('left', 'Left Aligned'),
        ('right', 'Right Aligned'),
        ('full', 'Full Width'),
    ], default='full')

    class Meta:
        template = "articles/blocks/image_block.html"
        icon = "image"
