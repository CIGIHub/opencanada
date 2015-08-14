# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0037_articlepage_hide_author_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='primary_topic',
            field=models.ForeignKey(related_name='articles', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.Topic', null=True),
        ),
    ]
