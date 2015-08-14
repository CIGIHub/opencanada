# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0036_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='hide_author_block',
            field=models.BooleanField(default=False),
        ),
    ]
