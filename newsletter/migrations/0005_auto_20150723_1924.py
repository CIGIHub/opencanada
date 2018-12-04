# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import modelcluster.fields
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0004_auto_20150723_1914'),
        ('articles', '0026_auto_20150728_1823'),
    ]

    operations = [

        migrations.AlterModelOptions(
            name='newsletterexternalarticlelink',
            options={'ordering': ['sort_order']},
        ),
        migrations.RemoveField(
            model_name='newsletterexternalarticlelink',
            name='external_article',
        ),
        migrations.RemoveField(
            model_name='newsletterexternalarticlelink',
            name='id',
        ),
        migrations.RemoveField(
            model_name='newsletterexternalarticlelink',
            name='newsletter',
        ),
        migrations.AddField(
            model_name='newsletterexternalarticlelink',
            name='externalarticle_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='articles.ExternalArticlePage', on_delete=models.deletion.SET_NULL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newsletterexternalarticlelink',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='external_articles', default=1, to='newsletter.NewsletterPage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newsletterexternalarticlelink',
            name='sort_order',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
    ]
