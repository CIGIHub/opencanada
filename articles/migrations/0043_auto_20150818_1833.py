# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0042_externalarticlelistpage_articles_per_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='visualization',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='category',
            field=models.ForeignKey(related_name='articlepage', on_delete=django.db.models.deletion.SET_NULL, default=1, to='articles.ArticleCategory', null=True),
        ),
    ]
