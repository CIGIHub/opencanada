# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0034_auto_20150813_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriespage',
            name='cached_facebook_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='cached_last_updated',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='cached_twitter_count',
            field=models.IntegerField(default=0),
        ),
    ]
