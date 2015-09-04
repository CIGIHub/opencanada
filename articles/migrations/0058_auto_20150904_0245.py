# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0057_articlelistpage_filter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlelistpage',
            name='filter_for_interviews',
        ),
        migrations.RemoveField(
            model_name='articlelistpage',
            name='filter_for_visualizations',
        ),
    ]
