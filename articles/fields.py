from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.utils.html import format_html
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock

from interactives.models import Interactive
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
            ('PullQuote', PullQuoteBlock()),
            ('Quote', SimpleQuoteBlock()),
            ('Overflow', OverflowStreamBlock()),
            ('ColumnedContent', ColumnarStreamBlock()),
            ('Interactive', InteractiveBlock(Interactive, icon="cogs")),
            ('RelatedItems', RelatedItemsBlock()),
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


class PullQuoteBlock(blocks.TextBlock):
    class Meta:
        template = "articles/blocks/pull_quote.html"
        icon = "openquote"


class SimpleQuoteBlock(blocks.RichTextBlock):
    class Meta:
        template = "articles/blocks/quote.html"
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
        ('editorial', 'Full Width Editorial'),
    ], default='full')
    expandable = blocks.BooleanBlock(default=False, required=False)
    label = blocks.CharBlock(required=False, help_text="Additional label to be displayed with the image.")

    class Meta:
        template = "articles/blocks/image_block.html"
        icon = "image"


class ChapterField(StreamField):
    def __init__(self, block_types=None, **kwargs):
        block_types = [
            ('chapter', ChapterBodyBlock()),
        ]

        super(ChapterField, self).__init__(block_types, **kwargs)


class InteractiveBlock(SnippetChooserBlock):
    def render(self, value):
        """
        Return a text rendering of 'value', suitable for display on templates. By default, this will
        use a template if a 'template' property is specified on the block, and fall back on render_basic
        otherwise.
        """
        template = value.template
        if template:
            return render_to_string(template, {'self': value})
        else:
            return self.render_basic(value)


class RelatedItemsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(default="Related")
    items = blocks.ListBlock(blocks.PageChooserBlock(label="item"))

    def __init__(self, **kwargs):
        super(RelatedItemsBlock, self).__init__(icon="list-ul", **kwargs)

    class Meta:
        template = "articles/blocks/related_items_block.html"


class SimpleBodyBlock(blocks.StreamBlock):
    Heading = HeadingBlock()
    Paragraph = ParagraphBlock()
    Image = ImageBlock()
    Embed = EmbedBlock(icon="site")
    List = blocks.ListBlock(blocks.RichTextBlock(label="item"), icon="list-ul")
    Sharable = SharableBlock()
    PullQuote = PullQuoteBlock()
    Quote = SimpleQuoteBlock()
    Interactive = InteractiveBlock(Interactive)
    RelatedItems = RelatedItemsBlock()


class ColumnarStreamBlock(blocks.StructBlock):
    body = SimpleBodyBlock(required=False)

    class Meta:
        template = "articles/blocks/columnar.html"


class ColumnBodyBlock(SimpleBodyBlock):
    ColumnedContent = ColumnarStreamBlock()


class OverflowStreamBlock(blocks.StructBlock):
    body = ColumnBodyBlock(required=False)

    class Meta:
        template = "articles/blocks/overflow.html"


class BodyBlock(SimpleBodyBlock):
    Overflow = OverflowStreamBlock()
    ColumnedContent = ColumnarStreamBlock()


class ChapterBodyBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    body = BodyBlock(required=False)

    class Meta:
        template = "articles/blocks/chapter.html"
        # icon = "openquote"


class EndNoteBlock(blocks.StructBlock):
    identifier = blocks.CharBlock()
    text = blocks.TextBlock()

    class Meta:
        template = "articles/blocks/endnote.html"


class CitationBlock(blocks.StructBlock):
    text = blocks.TextBlock()

    class Meta:
        template = "articles/blocks/citation.html"
