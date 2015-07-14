from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property
from django.utils.html import format_html
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock

from people.models import ContributorPage


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


class ContributorChooser(blocks.ChooserBlock):
    @cached_property
    def target_model(self):
        return ContributorPage

    @cached_property
    def widget(self):
        from wagtail.wagtailadmin.widgets import AdminPageChooser
        return AdminPageChooser(content_type=ContentType.objects.get_for_model(ContributorPage))

    def render_basic(self, value):
        if value:
            return format_html('<a href="{0}">{1}</a>', value.url, value.title)
        else:
            return ''


class AuthorBlurbBlock(blocks.StructBlock):
    author = ContributorChooser()
    number_of_articles = blocks.CharBlock(default=3)

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
