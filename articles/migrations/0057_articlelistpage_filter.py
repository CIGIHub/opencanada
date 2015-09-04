# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0056_auto_20150903_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlelistpage',
            name='filter',
            field=models.TextField(blank=True, null=True, choices=[('visualizations', 'Visualizations'), ('interviews', 'Interviews'), ('editors_pick', "Editor's Pick")]),
        ),
    ]
