# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0078_articlepage_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlepage',
            name='image_overlay_color',
        ),
        migrations.RemoveField(
            model_name='externalarticlepage',
            name='image_overlay_color',
        ),
        migrations.RemoveField(
            model_name='headline',
            name='image_overlay_color',
        ),
        migrations.RemoveField(
            model_name='seriespage',
            name='image_overlay_color',
        ),
    ]
