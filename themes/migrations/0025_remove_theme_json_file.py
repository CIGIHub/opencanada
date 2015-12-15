# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0024_auto_20151210_2148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='json_file',
        ),
    ]
