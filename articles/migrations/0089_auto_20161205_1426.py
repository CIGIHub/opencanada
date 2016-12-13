# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0088_responsearticlelink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsearticlelink',
            name='response',
            field=models.ForeignKey(related_name='response_to_links', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.ArticlePage', null=True),
        ),
        migrations.AlterField(
            model_name='responsearticlelink',
            name='response_to',
            field=modelcluster.fields.ParentalKey(related_name='response_links', to='articles.ArticlePage'),
        ),
    ]
