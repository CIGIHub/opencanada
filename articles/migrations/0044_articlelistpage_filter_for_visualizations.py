# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0043_auto_20150818_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlelistpage',
            name='filter_for_visualizations',
            field=models.BooleanField(default=False),
        ),
    ]
