# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150721_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchsuggestion',
            name='sort_order',
            field=models.IntegerField(default=0),
        ),
    ]
