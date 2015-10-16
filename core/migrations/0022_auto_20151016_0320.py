# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models

import themes.models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0016_auto_20151014_2016'),
        ('wagtailcore', '0019_verbose_names_cleanup'),
        ('core', '0021_streampage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streampage',
            name='id',
        ),
        migrations.AddField(
            model_name='streampage',
            name='page_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='wagtailcore.Page'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='streampage',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=themes.models.get_default_theme, to='themes.Theme', null=True),
        ),
    ]
