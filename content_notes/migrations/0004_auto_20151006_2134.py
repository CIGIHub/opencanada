# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import content_notes.models


class Migration(migrations.Migration):

    dependencies = [
        ('content_notes', '0003_auto_20150930_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endnote',
            name='uuid',
            field=models.CharField(default=content_notes.models.get_uuid, max_length=64, blank=True),
        ),
    ]
