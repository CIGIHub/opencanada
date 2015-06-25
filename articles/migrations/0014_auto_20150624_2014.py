# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_auto_20150624_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleTopicLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article', modelcluster.fields.ParentalKey(related_name='topic_links', to='articles.ArticlePage')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
            ],
        ),
        migrations.AddField(
            model_name='articletopiclink',
            name='topic',
            field=models.ForeignKey(related_name='article_links', to='articles.Topic'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='primary_topic',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.Topic', null=True),
        ),
        migrations.AddField(
            model_name='indepthpage',
            name='primary_topic',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.Topic', null=True),
        ),
    ]
