# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0062_auto_20150930_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='EndNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('text', wagtail.core.fields.RichTextField()),
                ('uuid', models.CharField(max_length=64, null=True, blank=True)),
                ('article', modelcluster.fields.ParentalKey(related_name='endnote_links', on_delete=django.db.models.deletion.SET_NULL, to='articles.ArticlePage', null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
