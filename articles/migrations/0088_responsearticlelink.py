# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0087_seriespage_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResponseArticleLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('response', models.ForeignKey(related_name='response_links', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.ArticlePage', null=True)),
                ('response_to', modelcluster.fields.ParentalKey(related_name='response_to_links', to='articles.ArticlePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
