# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0055_auto_20150903_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriespage',
            name='full_bleed_image_size',
            field=models.PositiveSmallIntegerField(default=75, help_text="Enter a value from 0 - 100, indicating the percentage of the screen to use for the full-bleed image layout. This value is only used if 'Use Main Image Full-Bleed Layout' is checked."),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='include_main_image_overlay',
            field=models.BooleanField(default=False, help_text='Check to use a full-bleed image layout.', verbose_name='Use Main Image Full-Bleed Layout'),
        ),
    ]
