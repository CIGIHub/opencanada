# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0003_auto_20150723_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalSourceLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsletterExternalArticleLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RenameField(
            model_name='externalarticle',
            old_name='article_link',
            new_name='website_link',
        ),
        migrations.AddField(
            model_name='newsletterexternalarticlelink',
            name='external_article',
            field=models.ForeignKey(related_name='newsletter_links', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='newsletter.ExternalArticle', null=True),
        ),
        migrations.AddField(
            model_name='newsletterexternalarticlelink',
            name='newsletter',
            field=modelcluster.fields.ParentalKey(related_name='external_links', to='newsletter.NewsletterPage'),
        ),
        migrations.AddField(
            model_name='externalsourcelink',
            name='external_article',
            field=modelcluster.fields.ParentalKey(related_name='source_link', to='newsletter.ExternalArticle'),
        ),
        migrations.AddField(
            model_name='externalsourcelink',
            name='source',
            field=models.ForeignKey(related_name='external_article_links', to='newsletter.Source'),
        ),
    ]
