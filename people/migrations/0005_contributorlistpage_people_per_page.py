# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_auto_20150706_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributorlistpage',
            name='people_per_page',
            field=models.IntegerField(default=20),
        ),
    ]
