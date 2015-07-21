# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordpress_importer', '0004_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='postimport',
            name='original_permalink',
            field=models.CharField(default='', max_length=2048),
        ),
    ]
