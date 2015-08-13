# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0029_auto_20150805_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='editors_pick',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='externalarticlepage',
            name='editors_pick',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='editors_pick',
            field=models.BooleanField(default=False),
        ),
    ]
