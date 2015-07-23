# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0022_create_feature_styles'),
    ]

    operations = [
        migrations.AddField(
            model_name='article_page',
            name='feature_style',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=1, to='articles.FeatureStyle', null=True),
        ),
        migrations.AddField(
            model_name='headline',
            name='feature_style',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=1, to='articles.FeatureStyle', null=True),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='feature_style',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=1, to='articles.FeatureStyle', null=True),
        ),
    ]
