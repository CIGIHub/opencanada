# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_auto_20150713_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlepage',
            name='subtitle',
        ),
    ]
