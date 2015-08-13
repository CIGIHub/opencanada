# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0032_auto_20150813_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='last_updated',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
