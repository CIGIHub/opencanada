# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0077_seriespage_video_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='video',
            field=models.BooleanField(default=False),
        ),
    ]
