# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models

import themes.models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0001_initial'),
        ('articles', '0058_auto_20150904_0245'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=themes.models.get_default_theme, to='themes.Theme', null=True),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=themes.models.get_default_theme, to='themes.Theme', null=True),
        ),
        migrations.AlterField(
            model_name='articlelistpage',
            name='filter',
            field=models.TextField(blank=True, null=True, choices=[('visualizations', 'Visualizations'), ('interviews', 'Interviews'), ('editors_pick', "Editor's Pick"), ('most_popular', 'Most Popular')]),
        ),
    ]
