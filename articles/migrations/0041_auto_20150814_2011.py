# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0040_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlelistpage',
            name='articles_per_page',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='serieslistpage',
            name='series_per_page',
            field=models.IntegerField(default=5),
        ),
    ]
