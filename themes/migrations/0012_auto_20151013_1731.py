# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0011_theme_backgroundimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='backgroundImage',
        ),
        migrations.AddField(
            model_name='themecontent',
            name='backgroundImage',
            field=models.ForeignKey(blank=True, to='themes.BackgroundImageBlock', null=True),
        ),
    ]
