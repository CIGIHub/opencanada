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
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleAuthorLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleListPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subtitle', wagtail.wagtailcore.fields.RichTextField(default='', blank=True)),
                ('body', articles.fields.BodyField([('Heading', wagtail.wagtailcore.blocks.CharBlock(classname='heading', icon='title')), ('Paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='doc-full')), ('Image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon='image')), ('Embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon='site')), ('List', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.RichTextBlock(label='item'), icon='list-ul')), ('Sharable', articles.fields.SharableBlock())])),
                ('excerpt', wagtail.wagtailcore.fields.RichTextField(default='', blank=True)),
                ('main_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ArticleTopicLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article', modelcluster.fields.ParentalKey(related_name='topic_links', to='articles.ArticlePage')),
            ],
        ),
        migrations.CreateModel(
            name='SeriesArticleLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('override_text', wagtail.wagtailcore.fields.RichTextField(default='', help_text='This field is optional. If not provided, the text will be pulled from the article page automatically. This field allows you to override the automatic text.', blank=True)),
                ('article', models.ForeignKey(related_name='series_links', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.ArticlePage', null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SeriesListPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SeriesPage',
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
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
            ],
        ),
        migrations.AddField(
            model_name='seriespage',
            name='primary_topic',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.Topic', null=True),
        ),
        migrations.AddField(
            model_name='seriesarticlelink',
            name='series',
            field=modelcluster.fields.ParentalKey(related_name='related_article_links', to='articles.SeriesPage'),
        ),
        migrations.AddField(
            model_name='seriesarticlelink',
            name='override_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', help_text='This field is optional. If not provided, the image will be pulled from the article page automatically. This field allows you to override the automatic image.', null=True),
        ),
        migrations.AddField(
            model_name='articletopiclink',
            name='topic',
            field=models.ForeignKey(related_name='article_links', to='articles.Topic'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='primary_topic',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.Topic', null=True),
        ),
        migrations.AddField(
            model_name='articleauthorlink',
            name='article',
            field=modelcluster.fields.ParentalKey(related_name='author_links', to='articles.ArticlePage'),
        ),
    ]
