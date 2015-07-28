# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0002_auto_20150723_1822'),
        ('articles', '0026_auto_20150728_1823'),
    ]

    operations = [

        migrations.CreateModel(
            name='NewsletterExternalArticleLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='newsletterexternalarticlelink',
            name='external_article',
            field=models.ForeignKey(related_name='newsletter_links', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.ExternalArticlePage', null=True),
        ),
        migrations.AddField(
            model_name='newsletterexternalarticlelink',
            name='newsletter',
            field=modelcluster.fields.ParentalKey(related_name='external_links', to='newsletter.NewsletterPage'),
        ),

    ]
