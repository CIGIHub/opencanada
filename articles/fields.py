from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import UploadedFile
from django.db.models import FileField
from django.forms import Field
from django.forms.widgets import Widget
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.utils.html import format_html
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from interactives.models import Interactive
from people.models import ContributorPage
from themes.blocks import ThemeableStructBlock


class BodyField(StreamField):
    def __init__(self, block_types=None, **kwargs):
        block_types = [
            ('Heading', HeadingBlock()),
            ('Paragraph', ParagraphBlock()),
            ('Image', ImageBlock()),
            ('Document', DocumentBlock()),
            ('Embed', EmbedBlock(icon="site")),
            ('List', blocks.ListBlock(
                blocks.RichTextBlock(label="item"), icon="list-ul")
             ),
            ('Sharable', SharableBlock()),
            ('PullQuote', PullQuoteBlock()),
            ('Quote', SimpleQuoteBlock()),
            ('Overflow', OverflowStreamBlock()),
            ('FullBleed', FullBleedStreamBlock()),
            ('ColumnedContent', ColumnarStreamBlock()),
            ('Interactive', InteractiveBlock(Interactive, icon="cogs")),
            ('RelatedItems', RelatedItemsBlock()),
            ('SectionBreak', SectionBreakBlock()),
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
        from wagtail.admin.widgets import AdminPageChooser
        return AdminPageChooser(content_type=ContentType.objects.get_for_model(ContributorPage))

    def render_basic(self, value, context=None):
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
        ('nocrop', 'Full Width - No Cropping')
    ], default='full')
    include_border = blocks.BooleanBlock(default=False, required=False)
    expandable = blocks.BooleanBlock(default=False, required=False)
    profile_image = blocks.BooleanBlock(
        default=False,
        required=False,
        help_text="Displays as a circular image, with a max-width of 200px when left or right aligned."
    )
    label = blocks.CharBlock(required=False, help_text="Additional label to be displayed with the image.")

    class Meta:
        template = "articles/blocks/image_block.html"
        icon = "image"


class DocumentBlock(blocks.StructBlock):
    document = DocumentChooserBlock()

    class Meta:
        template = "articles/blocks/document_block.html"
        icon = 'doc-full-inverse'


class ChapterField(StreamField):
    def __init__(self, block_types=None, **kwargs):
        block_types = [
            ('chapter', ChapterBodyBlock()),
        ]

        super(ChapterField, self).__init__(block_types, **kwargs)


class InteractiveBlock(SnippetChooserBlock):
    def render(self, value, context=None):
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


class RelatedItemsBlock(ThemeableStructBlock):
    heading = blocks.CharBlock(default="Related")
    items = blocks.ListBlock(blocks.PageChooserBlock(label="item"))

    def __init__(self, **kwargs):
        super(RelatedItemsBlock, self).__init__(icon="list-ul", **kwargs)

    class Meta:
        template = "articles/blocks/related_items_block.html"


class StaticHTMLInput(Widget):
    """
    Need an <input> widget that doesn't actually accept any input
    """
    input_type = 'hidden'

    def __init__(self, raw_html=None, **kwargs):
        self.raw_html = raw_html
        super(StaticHTMLInput, self).__init__(**kwargs)

    def render(self, name, value, attrs=None):
        if self.raw_html is not None:
            return format_html(self.raw_html)
        else:
            return ''


class StaticHTMLField(Field):
    def __init__(self, raw_html=None, **kwargs):
        widget = StaticHTMLInput(raw_html=raw_html)
        super(StaticHTMLField, self).__init__(widget=widget, **kwargs)


class StaticHTMLBlock(blocks.FieldBlock):
    def __init__(self, raw_html=None, required=False, help_text=None, **kwargs):
        self.raw_html = raw_html
        self.field = StaticHTMLField(raw_html=self.raw_html, required=required, help_text=help_text)
        super(StaticHTMLBlock, self).__init__(**kwargs)

    def render(self, value, context=None):
        """
        Return a text rendering of 'value', suitable for display on templates.
        Note that we override this function so that we can render the raw HTML as this block
        is just a container; 'value' in this case will always be None
        """
        if self.raw_html is not None:
            return format_html(self.raw_html)
        else:
            return ''


class SectionBreakBlock(blocks.StructBlock):
    section_break = StaticHTMLBlock(raw_html='<hr>')

    def render(self, value, context=None):
        """
        Return a text rendering of 'value', suitable for display on templates.
        Note that we override this function so that we can render the child block as this block
        is just a container; 'value' in this case will always be None
        """
        return self.child_blocks['section_break'].render(value)

    class Meta:
        icon = "code"


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
    SectionBreak = SectionBreakBlock()


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


class FullBleedStreamBlock(blocks.StructBlock):
    body = ColumnBodyBlock(required=False)

    class Meta:
        template = "articles/blocks/fullbleed.html"


class BodyBlock(SimpleBodyBlock):
    Overflow = OverflowStreamBlock()
    FullBleed = FullBleedStreamBlock()
    ColumnedContent = ColumnarStreamBlock()


class ChapterBodyBlock(ThemeableStructBlock):
    heading = blocks.CharBlock()
    body = BodyBlock(required=False)
    share_this_chapter = blocks.BooleanBlock(help_text="Check to include share links for this chapter for twitter and facebook.", required=False)
    tweet_text = blocks.CharBlock(help_text="Tweet to share, including hashtags (if any); if empty the tweet will contain just the URL link to this chapter.", max_length=140, required=False)

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


class WagtailFileField(FileField):
    '''
    We override this so that an uploaded file is always saved to storage when saving a draft of a Page
    '''
    def save_form_data(self, instance, data):
        super(WagtailFileField, self).save_form_data(instance, data)
        if isinstance(data, UploadedFile):
            super(WagtailFileField, self).pre_save(instance, False)
