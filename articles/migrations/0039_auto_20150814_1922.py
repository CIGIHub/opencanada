# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0038_auto_20150814_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seriespage',
            name='primary_topic',
            field=models.ForeignKey(related_name='series', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.Topic', null=True),
        ),
    ]
