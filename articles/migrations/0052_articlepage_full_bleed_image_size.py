# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0051_auto_20150903_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='full_bleed_image_size',
            field=models.PositiveSmallIntegerField(default=75),
        ),
    ]
