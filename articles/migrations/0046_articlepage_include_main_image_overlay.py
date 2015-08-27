# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0045_seriespage_include_main_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='include_main_image_overlay',
            field=models.BooleanField(default=False),
        ),
    ]
