# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0044_articlelistpage_filter_for_visualizations'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriespage',
            name='include_main_image',
            field=models.BooleanField(default=True),
        ),
    ]
