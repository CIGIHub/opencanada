# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_notes', '0004_auto_20151006_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endnote',
            name='uuid',
            field=models.CharField(max_length=64, blank=True),
        ),
    ]
