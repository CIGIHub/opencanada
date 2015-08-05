# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailimages.blocks
import articles.fields
import django.db.models.deletion
import wagtail.wagtailcore.blocks
import wagtail.wagtailembeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0028_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChapteredArticlePage',
            fields=[
                ('articlepage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='articles.ArticlePage')),
                ('chapters', articles.fields.ChapterField([('chapter', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock()), (b'body', wagtail.wagtailcore.blocks.StreamBlock([(b'Heading', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock()), (b'heading_level', wagtail.wagtailcore.blocks.ChoiceBlock(default=2, choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')]))])), (b'Paragraph', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.RichTextBlock()), (b'use_dropcap', wagtail.wagtailcore.blocks.BooleanBlock(required=False))])), (b'Image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'placement', wagtail.wagtailcore.blocks.ChoiceBlock(default='full', choices=[('left', 'Left Aligned'), ('right', 'Right Aligned'), ('full', 'Full Width')]))])), (b'Embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon='site')), (b'List', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.RichTextBlock(label='item'), icon='list-ul')), (b'Sharable', articles.fields.SharableBlock()), (b'AuthorBlurb', wagtail.wagtailcore.blocks.StructBlock([(b'author', articles.fields.ContributorChooser()), (b'number_of_articles', wagtail.wagtailcore.blocks.CharBlock(default=3))]))], required=False))]))], null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('articles.articlepage',),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='category',
            field=models.ForeignKey(related_name='articlepage', on_delete=django.db.models.deletion.SET_NULL, to='articles.ArticleCategory', null=True),
        ),
    ]
