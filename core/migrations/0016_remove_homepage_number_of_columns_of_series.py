# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20150903_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='number_of_columns_of_series',
        ),
    ]
