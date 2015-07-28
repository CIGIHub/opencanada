# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0026_auto_20150728_1823'),
        ('newsletter', '0009_auto_20150724_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletterexternalarticlelink',
            name='externalarticle_ptr',
        ),
        migrations.RemoveField(
            model_name='newsletterexternalarticlelink',
            name='page',
        ),
        migrations.AddField(
            model_name='newsletterexternalarticlelink',
            name='article_text',
            field=wagtail.wagtailcore.fields.RichTextField(default='', help_text='Text to describe article.', blank=True),
        ),
        migrations.AddField(
            model_name='newsletterexternalarticlelink',
            name='external_article',
            field=models.ForeignKey(related_name='newsletter_links', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.ExternalArticlePage', help_text='Link to an external article', null=True),
        ),
        migrations.AddField(
            model_name='newsletterexternalarticlelink',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newsletterexternalarticlelink',
            name='newsletter',
            field=modelcluster.fields.ParentalKey(related_name='external_article_links', default=1, to='newsletter.NewsletterPage'),
            preserve_default=False,
        ),
    ]
