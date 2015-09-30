# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0062_auto_20150930_1633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citation',
            name='article',
        ),
        migrations.DeleteModel(
            name='Citation',
        ),
    ]
