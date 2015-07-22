# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0018_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='sticky',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='sticky',
            field=models.BooleanField(default=False),
        ),
    ]
