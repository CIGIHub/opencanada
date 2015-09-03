# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20150903_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='full_bleed_image_size',
            field=models.PositiveSmallIntegerField(default=90),
        ),
    ]
