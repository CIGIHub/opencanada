# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_auto_20150707_2303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlepage',
            name='subtitle',
        ),
    ]
