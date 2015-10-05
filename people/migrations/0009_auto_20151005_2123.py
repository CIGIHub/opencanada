# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models

import themes.models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0006_create_themes'),
        ('people', '0008_auto_20150904_0211'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributorlistpage',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=themes.models.get_default_theme, to='themes.Theme', null=True),
        ),
        migrations.AddField(
            model_name='contributorpage',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=themes.models.get_default_theme, to='themes.Theme', null=True),
        ),
    ]
