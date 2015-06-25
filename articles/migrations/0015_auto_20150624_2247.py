# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_auto_20150624_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indeptharticlelink',
            name='article',
            field=models.ForeignKey(related_name='in_depth_links', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.ArticlePage', null=True),
        ),
        migrations.AlterField(
            model_name='indeptharticlelink',
            name='in_depth',
            field=modelcluster.fields.ParentalKey(related_name='related_article_links', to='articles.InDepthPage'),
        ),
    ]
