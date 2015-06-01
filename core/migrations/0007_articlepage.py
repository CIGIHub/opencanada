# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('people', '0002_auto_20150525_1813'),
        ('core', '0006_create_features_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subtitle', models.TextField(default='', blank=True)),
                ('body', wagtail.wagtailcore.fields.StreamField([('Heading', wagtail.wagtailcore.blocks.CharBlock(classname='heading')), ('Text', wagtail.wagtailcore.blocks.RichTextBlock()), ('Image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('Embed', wagtail.wagtailembeds.blocks.EmbedBlock())])),
                ('author', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='people.Contributor', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
