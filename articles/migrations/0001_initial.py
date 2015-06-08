# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks
from django.db import migrations, models

import articles.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('people', '0003_contributor_headshot'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subtitle', wagtail.wagtailcore.fields.RichTextField(default='', blank=True)),
                ('body', articles.fields.BodyField([('Heading', wagtail.wagtailcore.blocks.CharBlock(classname='heading', icon='title')), ('Text', wagtail.wagtailcore.blocks.RichTextBlock(icon='doc-full')), ('Image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon='image')), ('Embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon='site')), ('List', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.RichTextBlock(label='item'), icon='list-ul')), ('Sharable', wagtail.wagtailcore.blocks.CharBlock(icon='openquote'))])),
                ('author', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='people.Contributor', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
