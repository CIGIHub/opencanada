# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0008_auto_20150723_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(verbose_name='Event Date'),
        ),
        migrations.AlterField(
            model_name='newsletterarticlelink',
            name='article',
            field=models.ForeignKey(related_name='newsletter_links', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.ArticlePage', help_text='Link to an internal article', null=True),
        ),
        migrations.AlterField(
            model_name='newslettereventlink',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='events', to='newsletter.NewsletterPage'),
        ),
    ]
