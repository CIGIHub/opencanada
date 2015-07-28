# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('articles', '0024_auto_20150722_1928'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterArticleLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('override_text', wagtail.wagtailcore.fields.RichTextField(default='', help_text='Text to describe article.', blank=True)),
                ('article', models.ForeignKey(related_name='newsletter_links', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.ArticlePage', null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewsletterPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('issue_date', models.DateField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='newsletterarticlelink',
            name='newsletter',
            field=modelcluster.fields.ParentalKey(related_name='article_links', to='newsletter.NewsletterPage'),
        ),
        migrations.AddField(
            model_name='newsletterarticlelink',
            name='override_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='images.AttributedImage', help_text='Circular Image to accompany article if article image not selected', null=True),
        ),
    ]
