# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='first_name',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='last_name',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
