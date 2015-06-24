# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_contributor_headshot'),
        ('articles', '0011_auto_20150623_1918'),
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
        migrations.RemoveField(
            model_name='articlepage',
            name='author',
        ),
        migrations.AddField(
            model_name='articleauthorlink',
            name='article',
            field=modelcluster.fields.ParentalKey(related_name='authors', to='articles.ArticlePage'),
        ),
        migrations.AddField(
            model_name='articleauthorlink',
            name='author',
            field=models.ForeignKey(related_name='articles', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='people.Contributor', null=True),
        ),
    ]
