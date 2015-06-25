# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_auto_20150623_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleauthorlink',
            name='article',
            field=modelcluster.fields.ParentalKey(related_name='author_links', to='articles.ArticlePage'),
        ),
        migrations.AlterField(
            model_name='articleauthorlink',
            name='author',
            field=models.ForeignKey(related_name='article_links', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='people.Contributor', null=True),
        ),
    ]
