# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks
from django.db import migrations, models

import articles.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('wagtailcore', '__latest__'),
        ('articles', '0005_articlepage_main_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='InDepthArticleLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', wagtail.wagtailcore.fields.RichTextField()),
                ('article', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.ArticlePage', null=True)),
                ('image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InDepthPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', articles.fields.BodyField([('Heading', wagtail.wagtailcore.blocks.CharBlock(classname='heading', icon='title')), ('Paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='doc-full')), ('Image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon='image')), ('Embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon='site')), ('List', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.RichTextBlock(label='item'), icon='list-ul')), ('Sharable', articles.fields.SharableBlock())], default='', blank=True)),
                ('image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='indeptharticlelink',
            name='in_depth',
            field=modelcluster.fields.ParentalKey(related_name='related_articles', to='articles.InDepthPage'),
        ),
    ]
