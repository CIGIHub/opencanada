# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
from django.db import migrations, models

import articles.fields
import interactives.models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0059_auto_20150923_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='Citation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('text', wagtail.core.fields.RichTextField()),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EndNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('text', wagtail.core.fields.RichTextField()),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='chapteredarticlepage',
            name='chapters',
        ),
        migrations.AddField(
            model_name='articlepage',
            name='chapters',
            field=articles.fields.ChapterField([('chapter', wagtail.core.blocks.StructBlock([(b'heading', wagtail.core.blocks.CharBlock()), (b'body', wagtail.core.blocks.StreamBlock([(b'Heading', wagtail.core.blocks.StructBlock([(b'text', wagtail.core.blocks.CharBlock()), (b'heading_level', wagtail.core.blocks.ChoiceBlock(default=2, choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')]))])), (b'Paragraph', wagtail.core.blocks.StructBlock([(b'text', wagtail.core.blocks.RichTextBlock()), (b'use_dropcap', wagtail.core.blocks.BooleanBlock(required=False))])), (b'Image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'placement', wagtail.core.blocks.ChoiceBlock(default='full', choices=[('left', 'Left Aligned'), ('right', 'Right Aligned'), ('full', 'Full Width'), ('editorial', 'Full Width Editorial')])), (b'expandable', wagtail.core.blocks.BooleanBlock(default=False, required=False)), (b'label', wagtail.core.blocks.CharBlock(help_text='Additional label to be displayed with the image.', required=False))])), (b'Embed', wagtail.embeds.blocks.EmbedBlock(icon='site')), (b'List', wagtail.core.blocks.ListBlock(wagtail.core.blocks.RichTextBlock(label='item'), icon='list-ul')), (b'Sharable', articles.fields.SharableBlock()), (b'PullQuote', articles.fields.PullQuoteBlock()), (b'Quote', articles.fields.SimpleQuoteBlock()), (b'Interactive', articles.fields.InteractiveBlock(interactives.models.Interactive)), (b'RelatedItems', wagtail.core.blocks.StructBlock([(b'heading', wagtail.core.blocks.CharBlock(default='Related')), (b'items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock(label='item')))], icon='list-ul')), (b'Overflow', wagtail.core.blocks.StructBlock([(b'body', wagtail.core.blocks.StreamBlock([(b'Heading', wagtail.core.blocks.StructBlock([(b'text', wagtail.core.blocks.CharBlock()), (b'heading_level', wagtail.core.blocks.ChoiceBlock(default=2, choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')]))])), (b'Paragraph', wagtail.core.blocks.StructBlock([(b'text', wagtail.core.blocks.RichTextBlock()), (b'use_dropcap', wagtail.core.blocks.BooleanBlock(required=False))])), (b'Image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'placement', wagtail.core.blocks.ChoiceBlock(default='full', choices=[('left', 'Left Aligned'), ('right', 'Right Aligned'), ('full', 'Full Width'), ('editorial', 'Full Width Editorial')])), (b'expandable', wagtail.core.blocks.BooleanBlock(default=False, required=False)), (b'label', wagtail.core.blocks.CharBlock(help_text='Additional label to be displayed with the image.', required=False))])), (b'Embed', wagtail.embeds.blocks.EmbedBlock(icon='site')), (b'List', wagtail.core.blocks.ListBlock(wagtail.core.blocks.RichTextBlock(label='item'), icon='list-ul')), (b'Sharable', articles.fields.SharableBlock()), (b'PullQuote', articles.fields.PullQuoteBlock()), (b'Quote', articles.fields.SimpleQuoteBlock()), (b'Interactive', articles.fields.InteractiveBlock(interactives.models.Interactive)), (b'RelatedItems', wagtail.core.blocks.StructBlock([(b'heading', wagtail.core.blocks.CharBlock(default='Related')), (b'items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock(label='item')))], icon='list-ul')), (b'ColumnedContent', wagtail.core.blocks.StructBlock([(b'body', wagtail.core.blocks.StreamBlock([(b'Heading', wagtail.core.blocks.StructBlock([(b'text', wagtail.core.blocks.CharBlock()), (b'heading_level', wagtail.core.blocks.ChoiceBlock(default=2, choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')]))])), (b'Paragraph', wagtail.core.blocks.StructBlock([(b'text', wagtail.core.blocks.RichTextBlock()), (b'use_dropcap', wagtail.core.blocks.BooleanBlock(required=False))])), (b'Image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'placement', wagtail.core.blocks.ChoiceBlock(default='full', choices=[('left', 'Left Aligned'), ('right', 'Right Aligned'), ('full', 'Full Width'), ('editorial', 'Full Width Editorial')])), (b'expandable', wagtail.core.blocks.BooleanBlock(default=False, required=False)), (b'label', wagtail.core.blocks.CharBlock(help_text='Additional label to be displayed with the image.', required=False))])), (b'Embed', wagtail.embeds.blocks.EmbedBlock(icon='site')), (b'List', wagtail.core.blocks.ListBlock(wagtail.core.blocks.RichTextBlock(label='item'), icon='list-ul')), (b'Sharable', articles.fields.SharableBlock()), (b'PullQuote', articles.fields.PullQuoteBlock()), (b'Quote', articles.fields.SimpleQuoteBlock()), (b'Interactive', articles.fields.InteractiveBlock(interactives.models.Interactive)), (b'RelatedItems', wagtail.core.blocks.StructBlock([(b'heading', wagtail.core.blocks.CharBlock(default='Related')), (b'items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock(label='item')))], icon='list-ul'))], required=False))]))], required=False))])), (b'ColumnedContent', wagtail.core.blocks.StructBlock([(b'body', wagtail.core.blocks.StreamBlock([(b'Heading', wagtail.core.blocks.StructBlock([(b'text', wagtail.core.blocks.CharBlock()), (b'heading_level', wagtail.core.blocks.ChoiceBlock(default=2, choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')]))])), (b'Paragraph', wagtail.core.blocks.StructBlock([(b'text', wagtail.core.blocks.RichTextBlock()), (b'use_dropcap', wagtail.core.blocks.BooleanBlock(required=False))])), (b'Image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'placement', wagtail.core.blocks.ChoiceBlock(default='full', choices=[('left', 'Left Aligned'), ('right', 'Right Aligned'), ('full', 'Full Width'), ('editorial', 'Full Width Editorial')])), (b'expandable', wagtail.core.blocks.BooleanBlock(default=False, required=False)), (b'label', wagtail.core.blocks.CharBlock(help_text='Additional label to be displayed with the image.', required=False))])), (b'Embed', wagtail.embeds.blocks.EmbedBlock(icon='site')), (b'List', wagtail.core.blocks.ListBlock(wagtail.core.blocks.RichTextBlock(label='item'), icon='list-ul')), (b'Sharable', articles.fields.SharableBlock()), (b'PullQuote', articles.fields.PullQuoteBlock()), (b'Quote', articles.fields.SimpleQuoteBlock()), (b'Interactive', articles.fields.InteractiveBlock(interactives.models.Interactive)), (b'RelatedItems', wagtail.core.blocks.StructBlock([(b'heading', wagtail.core.blocks.CharBlock(default='Related')), (b'items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock(label='item')))], icon='list-ul'))], required=False))]))], required=False))]))], null=True, blank=True),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='citations_heading',
            field=models.TextField(default='Works Cited', blank=True),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='endnote_identifier_style',
            field=models.CharField(default='roman-lower', max_length=20, choices=[('roman-lower', 'Roman Numerals - Lowercase'), ('roman-upper', 'Roman Numerals - Uppercase'), ('numbers', 'Numbers')]),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='endnotes_heading',
            field=models.TextField(default='End Notes', blank=True),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='table_of_contents_heading',
            field=models.TextField(default='Table of Contents', blank=True),
        ),
        migrations.AddField(
            model_name='endnote',
            name='article',
            field=modelcluster.fields.ParentalKey(related_name='endnote_links', to='articles.ArticlePage'),
        ),
        migrations.AddField(
            model_name='citation',
            name='article',
            field=modelcluster.fields.ParentalKey(related_name='citation_links', to='articles.ArticlePage'),
        ),
    ]
