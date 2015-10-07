# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20151005_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpostingpage',
            name='cached_facebook_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='jobpostingpage',
            name='cached_last_updated',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='jobpostingpage',
            name='cached_twitter_count',
            field=models.IntegerField(default=0),
        ),
    ]
