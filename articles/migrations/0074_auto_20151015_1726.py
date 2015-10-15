# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0073_auto_20151013_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='slippery',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='slippery_for_type_section',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='externalarticlepage',
            name='slippery',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='externalarticlepage',
            name='slippery_for_type_section',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='slippery',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='slippery_for_type_section',
            field=models.BooleanField(default=False),
        ),
    ]
