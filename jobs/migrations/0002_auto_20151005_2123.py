# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models

import themes.models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0006_create_themes'),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpostinglistpage',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=themes.models.get_default_theme, to='themes.Theme', null=True),
        ),
        migrations.AddField(
            model_name='jobpostingpage',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=themes.models.get_default_theme, to='themes.Theme', null=True),
        ),
    ]
