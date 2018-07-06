# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0028_merge'),
        ('newsletter', '0014_newsletterlistpage_intro_text'),
    ]

    operations = [
        # Temporarily used to restore missing table on production.
        # migrations.CreateModel(
        #     name='NewsletterExternalArticleLink',
        #     fields=[
        #         ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
        #         ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
        #         ('override_text', wagtail.core.fields.RichTextField(default='', help_text='Text to describe article.', blank=True)),
        #         ('external_article', models.ForeignKey(related_name='newsletter_links', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.ExternalArticlePage', help_text='Link to an external article', null=True)),
        #         ('newsletter', modelcluster.fields.ParentalKey(related_name='external_article_links', to='newsletter.NewsletterPage')),
        #     ],
        #     options={
        #         'ordering': ['sort_order'],
        #         'abstract': False,
        #     },
        # ),
    ]
