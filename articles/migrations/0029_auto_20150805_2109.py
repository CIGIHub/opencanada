# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import wagtail.core.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks
from django.db import migrations, models

import articles.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0028_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChapteredArticlePage',
            fields=[
                ('articlepage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='articles.ArticlePage', on_delete=django.db.models.deletion.CASCADE)),
                ('chapters', articles.fields.ChapterField([('chapter', wagtail.core.blocks.StructBlock([(b'heading', wagtail.core.blocks.CharBlock()), (b'body', wagtail.core.blocks.StreamBlock([(b'Heading', wagtail.core.blocks.StructBlock([(b'text', wagtail.core.blocks.CharBlock()), (b'heading_level', wagtail.core.blocks.ChoiceBlock(default=2, choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')]))])), (b'Paragraph', wagtail.core.blocks.StructBlock([(b'text', wagtail.core.blocks.RichTextBlock()), (b'use_dropcap', wagtail.core.blocks.BooleanBlock(required=False))])), (b'Image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'placement', wagtail.core.blocks.ChoiceBlock(default='full', choices=[('left', 'Left Aligned'), ('right', 'Right Aligned'), ('full', 'Full Width')]))])), (b'Embed', wagtail.embeds.blocks.EmbedBlock(icon='site')), (b'List', wagtail.core.blocks.ListBlock(wagtail.core.blocks.RichTextBlock(label='item'), icon='list-ul')), (b'Sharable', articles.fields.SharableBlock()), (b'AuthorBlurb', wagtail.core.blocks.StructBlock([(b'author', articles.fields.ContributorChooser()), (b'number_of_articles', wagtail.core.blocks.CharBlock(default=3))]))], required=False))]))], null=True, blank=True)),
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
