# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_create_indepth_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indeptharticlelink',
            name='article',
            field=models.ForeignKey(related_name='series', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.ArticlePage', null=True),
        ),
    ]
