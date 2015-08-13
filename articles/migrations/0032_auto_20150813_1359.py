# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0031_auto_20150812_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='cached_facebook_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='cached_twitter_count',
            field=models.IntegerField(default=0),
        ),
    ]
