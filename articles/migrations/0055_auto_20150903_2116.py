# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0054_seriespage_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='number_of_related_articles',
            field=models.PositiveSmallIntegerField(default=6, verbose_name='Number of Related Articles to Show'),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='number_of_related_articles',
            field=models.PositiveSmallIntegerField(default=6, verbose_name='Number of Related Articles to Show'),
        ),
    ]
